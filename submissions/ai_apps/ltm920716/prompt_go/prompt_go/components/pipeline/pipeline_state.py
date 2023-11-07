import reflex as rx
from prompt_go.states import State, ChatNode, Dataset, ChatRunRecord
from sqlalchemy.sql import func
from typing import Dict, List
import time

import requests
from collections import defaultdict
from ..utils import ToastProvider, openai_chat, INSTRUCTION_OUTPUT_EVAL, INSTRUCTION_EVAL


class PipelineState(State):
    default_node_version: str = '1'
    params_model = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4']
    node_temperature_value: str = '1.0'

    role_options: List[str] = ["system", "user", "assistant"]

    _node_name_exists: bool = False
    _new_node_form: dict
    init_node_page: bool = True

    def next_prompt_page(self, form_dict: dict):
        if not self._node_name_exists:
            self._new_node_form = form_dict
            self.init_node_page = False

    def back_node_page(self):
        self.init_node_page = True
        self.role_items = [{
            'index': "0",
            'role': "user",
            'content': "",
        }]
        self.role_track = {}
        self.content_track = {}

    role_track: Dict
    role_items: List[Dict[str, str]] = [{
        'index': "0",
        'role': "user",
        'content': "",
    }]
    content_track: Dict

    def save_role(self):
        """update the save"""
        for k, v in self.role_track.items():
            self.role_items[int(k)]['role'] = v
        for k, v in self.content_track.items():
            self.role_items[int(k)]['content'] = v

        with rx.session() as session:
            merge_dict = self._new_node_form
            merge_dict['prompts'] = str(self.role_items)
            merge_dict['username'] = self.username
            # merge_dict['created_at'] = func.now()
            merge_dict['api_temperature'] = int(
                merge_dict['api_temperature']) / 100
            session.add(ChatNode(created_at=func.now(), **merge_dict))
            session.commit()

            self.node_name = ''
            self.node_temperature_value = '1.0'
            self.back_node_page()

        return ToastProvider.show(
            title="create node successfully, see in left panel",
            description="",
            duration=3000,
            status="success"
        )

    node_select_check: bool = False

    def check_node_select(self):
        self.node_select_check = not (self.node_select_check)

    @rx.var
    def has_node(self) -> bool:
        with rx.session() as session:
            result = session.query(ChatNode.node_name.distinct()).all()
            if result:
                return True
            else:
                return False

    @rx.var
    def query_node_list(self) -> List[str]:
        """Get a list of node."""
        with rx.session() as session:
            result = session.query(ChatNode.node_name.distinct()).all()
            node_names = [name[0] for name in result]
            if node_names:
                self.has_node = True
            else:
                self.has_node = False

        return node_names

    node_name: str

    @rx.var
    def node_exists(self) -> bool:
        with rx.session() as session:
            res = session.query(ChatNode).filter(
                ChatNode.node_name == self.node_name).first()
            if res:
                self._node_name_exists = True
                return True

        self._node_name_exists = False
        return False

    def set_node_temperature(self, value: int):
        self.node_temperature_value = str(value / 100)

    @rx.var
    def default_temperature(self) -> int:
        return int(float(self.node_temperature_value)*100)

    def add_role(self) -> None:
        """Add a role."""
        self.role_items.append({
            'index': str(len(self.role_items)),
            'role': "user",
            'content': "",
        })

    def remove_role(self) -> None:
        """Remove a role."""

        if self.role_items:
            key = self.role_items[-1]['index']
            if key in self.role_track:
                del self.role_track[key]
            if key in self.content_track:
                del self.content_track[key]

            self.role_items.pop()

    def change_tmp(self, type, value, index) -> None:
        """track changed data"""
        if type == 'role':
            self.role_track[index] = value
        else:
            self.content_track[index] = value

    query_node_name: str = ''

    @rx.var
    def query_node_by_name(self) -> List[ChatNode]:
        with rx.session() as session:
            if self.query_node_name:
                res = session.query(ChatNode).filter(
                    ChatNode.node_name == self.query_node_name).all()
                for index in range(len(res)):
                    res[index].created_at = res[index].created_at.strftime(
                        "%Y-%m-%d %H:%M:%S")
            else:
                res = []

        return res

    _selected_node_item: List[ChatNode] = []
    selected_node_status: Dict[int, bool] = {}

    def set_select_node_item(self, val, node_item: ChatNode):
        # # note: create_at is str
        # if self._selected_node_item and (self.query_node_name != self._selected_node_item[0].get('node_name')):
        #     self._selected_node_item = []
        if val:
            self._selected_node_item.append(node_item)
            self.selected_node_status[node_item['id']] = True
        else:
            self._selected_node_item.remove(node_item)
            self.selected_node_status[node_item['id']] = False


    @rx.var
    def dataset_list(self) -> List[str]:
        with rx.session() as session:
            result = session.query(Dataset.dataset_name.distinct()).all()
            dataset_names = ['None'] + [name[0] for name in result]
        return dataset_names

    score_api: str = 'Manually'
    dataset_iteration: int = 1
    dataset_option: str = 'None'

    scoreAPI_list = ['Manually', 'AI-Score']
    open_run_chat: bool = False
    _chat_api_url = "https://api.openai.com/v1/completions"
    run_chat_progress: int = 0

    async def run_selected_node(self):
        if len(self._selected_node_item) != 1:
            self.node_select_check = True
            return

        self.run_chat_progress = 0
        self.open_run_chat = True
        yield

        selected_node_item = self._selected_node_item[0]
        chat_history = eval(selected_node_item['prompts'])
        temperature = float(selected_node_item['api_temperature'])
        model = selected_node_item['api_model']

        dataset = self.processing_dataset(self.dataset_option)

        chat_results = []
        all_num = len(eval(dataset['source'])) * self.dataset_iteration
        run_index = 1

        for source in eval(dataset["source"]):
            messages = []
            history_prompt = ''
            default_placeholder = defaultdict(
                lambda: '<a placeholder>', source.get("placeholders", {}))
            for message in chat_history:
                messages.append({
                    'role': message['role'],
                    'content': message['content'].format_map(default_placeholder)
                })
                history_prompt += '\n'+message['role']+': '+ message['content'].format_map(default_placeholder)

            if source.get("input"):
                messages.append({"role": "user", "content": source["input"]})
                history_prompt+= '\nuser: '+ source["input"]

            for _ in range(self.dataset_iteration):
                chat_result = await self.api_call(api_url=self._chat_api_url, model=model, temperature=temperature,
                                                  messages=messages)

                score = await self.get_run_score(self.score_api, history_prompt, chat_result, source.get('target', ''))

                result = {"output": chat_result,
                          "ori_score": score, "up_score": score}
                chat_results.append(result)

                self.run_chat_progress = round(run_index / all_num * 100)
                run_index += 1
                yield
        with rx.session() as session:
            save_data = ChatRunRecord(
                chat_result=str(chat_results),
                node_name=selected_node_item['node_name'],
                node_version=selected_node_item['node_version'],
                dataset=self.dataset_option,
                items=all_num,
                iteration=self.dataset_iteration,
                time_stamp=str(int(time.time() * 1000)),
                score_api=self.score_api
            )
            session.add(save_data)
            session.commit()

        self.open_run_chat = False

        yield ToastProvider.show(
            title="running done! Jupm to History and see the result.",
            description="",
            duration=3000,
            status="success"
        )

    def processing_dataset(self, dataset: str) -> list:
        # {"source": [{"placeholders": {"a": ""}, "input": "", "target": ""}]}
        if dataset == 'None' or not dataset:
            processed_dataset = {'dataset_name': 'None', 'source': str(
                [{"placeholders": {}, "input": "", "target": ""}])}
        else:
            with rx.session() as session:
                processed_dataset = session.query(Dataset).filter(
                    Dataset.dataset_name == self.dataset_option).first().dict()

        return processed_dataset

    async def api_call(self, api_url: str, **kwargs):
        """call api"""
        if api_url == "https://api.openai.com/v1/completions":
            res_message = openai_chat(kwargs.get("messages", []), kwargs.get("model", "gpt-3.5-turbo"), kwargs.get("temperature", 0.5))
        else:
            res_message = requests.post(api_url, json=kwargs).json()

        return res_message

    async def get_run_score(self, api: str, input: str, output: str, label: str) -> int:
        score = 0
        if api == 'AI-Score':
            # todo : optimize AI-Score API
            if label:
                prompt = INSTRUCTION_OUTPUT_EVAL.format(input_pred_gt_dict={'history_instruction': input, 'expected_output': label, 'last_output': output})
            else:
                prompt = INSTRUCTION_EVAL.format(input_pred_dict={'history_instruction': input, 'last_output': output})
                        
            messages = [{"role": "user", "content": prompt}]
            score = openai_chat(messages)
            try:
                score = round(float(score))
                assert score in [0, 1, 2, 3, 4, 5], f'score is: {score}, should be in [0, 1, 2, 3, 4, 5]'
            except:
                score = 0

        return score

    show_prompt_drawer: bool = False

    def prompt_drawer_close(self):
        self.show_prompt_drawer = False

    drawer_show_prompt: List[dict] = []
    drawer_show_param: dict = {}

    def show_prompt(self):
        if self._selected_node_item:
            if len(self._selected_node_item) != 1:
                self.drawer_show_prompt = [
                    {'role': 'warning', 'align': 'left', 'content': 'only check one record to view'}]
                self.drawer_show_param = {}
            else:
                selected_node_item = self._selected_node_item[0]
                self.drawer_show_param = {
                    'model': selected_node_item['api_model'], 'temperature': selected_node_item['api_temperature'], 'description': selected_node_item['description']}
                self.drawer_show_prompt = []
                for message in eval(selected_node_item['prompts']):
                    self.drawer_show_prompt.append(
                        {'role': message['role'], 'align': 'right' if message['role'] == 'assistant' else 'left', 'content': message['content']})
        else:
            self.drawer_show_prompt = [
                {'role': 'warning', 'align': 'left', 'content': 'check one record first to view'}]
            self.drawer_show_param = {}

        self.show_prompt_drawer = True

    open_version_modal: bool = False
    _new_version: str = ''
    new_api_model: str = 'gpt-3.5-turbo'
    new_description: str = ''
    default_api_model: str = ''
    default_description: str = ''

    def add_version(self):
        if len(self._selected_node_item) != 1:
            self.node_select_check = True
            return

        with rx.session() as session:
            result = session.query(ChatNode.node_version).filter(
                ChatNode.node_name == self.query_node_name).all()
            self._new_version = str(max([int(item[0]) for item in result]) + 1)

            selected_node_item = self._selected_node_item[0]
            self.role_items = []
            self.role_track = {}
            self.content_track = {}
            self.node_temperature_value = selected_node_item['api_temperature']
            self.default_api_model = selected_node_item['api_model']
            self.default_description = selected_node_item['description']
            for message in eval(selected_node_item['prompts']):
                self.role_items.append(
                    {'index': message['index'], 'role': message['role'], 'content': message['content']})

        self.open_version_modal = True

    def ok_version(self):
        for k, v in self.role_track.items():
            self.role_items[int(k)]['role'] = v
        for k, v in self.content_track.items():
            self.role_items[int(k)]['content'] = v

        with rx.session() as session:
            merge_dict = {}
            merge_dict['node_name'] = str(self.query_node_name)
            merge_dict['node_version'] = str(self._new_version)
            merge_dict['api_model'] = str(self.new_api_model)
            merge_dict['prompts'] = str(self.role_items)
            merge_dict['description'] = str(self.new_description)
            merge_dict['username'] = self.username
            merge_dict['api_temperature'] = self.node_temperature_value
            session.add(ChatNode(created_at=func.now(), **merge_dict))
            session.commit()

            self.node_temperature_value = '1.0'

        self.cancel_version()

    def cancel_version(self):
        self.role_items = [{
            'index': "0",
            'role': "user",
            'content': "",
        }]
        self.role_track = {}
        self.content_track = {}
        self.open_version_modal = False

    delete_confirm: bool = False

    def remove_version(self):
        if len(self._selected_node_item) != 1:
            self.node_select_check = True
            return

        self.delete_confirm = True

    def del_confirm_status(self, del_flag: bool):
        if del_flag:
            delete_item = self._selected_node_item[0]
            with rx.session() as session:
                # delete associated History Record
                session.query(ChatRunRecord).filter(ChatRunRecord.node_name ==
                                                    delete_item['node_name'], ChatRunRecord.node_version == delete_item['node_version']).delete()
                # delete node
                session.query(ChatNode).filter(
                    ChatNode.id == delete_item['id']).delete()
                session.commit()

            self._selected_node_item = []
            self.selected_node_status = {}

        self.delete_confirm = False

