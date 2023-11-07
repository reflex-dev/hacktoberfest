from prompt_go.states import State, ChatRunRecord, Dataset, ChatNode
import reflex as rx
from typing import List, Dict
import json
from ..utils import ToastProvider


class HistoryState(State):
    @rx.var
    def has_record(self) -> bool:
        with rx.session() as session:
            result = session.query(ChatRunRecord.node_name.distinct()).all()

            if result:
                return True
            else:
                return False

    @rx.var
    def query_history_list(self) -> List[str]:
        """Get a list of history."""
        with rx.session() as session:
            result = session.query(ChatRunRecord.node_name.distinct()).all()
            node_names = [name[0] for name in result]

        return node_names

    _history_node_name: str = ''

    def set_history_node_name(self, node_name):
        self._selected_history_item = {}
        self._history_node_name = node_name

    @rx.var
    def query_history_by_name(self) -> List[ChatRunRecord]:
        with rx.session() as session:
            if self._history_node_name:
                res = session.query(ChatRunRecord).filter(
                    ChatRunRecord.node_name == self._history_node_name).all()
            else:
                res = []

        return res

    @rx.var
    def selected_item_status(self) -> Dict[int, bool]:
        status = {}
        for item in self.query_history_by_name:
            if item.id in self._selected_history_item:
                status[item.id] = True
            else:
                status[item.id] = False
        return status

    _selected_history_item: Dict[int, ChatRunRecord] = {}
    check_max_compare: bool = False

    def close_check_max_compare(self):
        self.check_max_compare = False

    compare_error: bool = False

    def close_compare_error(self):
        self.compare_error = False

    def set_select_history_item(self, index, val, node_item: ChatRunRecord):
        # note: create_at is str
        if self._selected_history_item and (self._history_node_name != list(self._selected_history_item.values())[0].get('node_name')):
            self._selected_history_item = {}

        if val:
            if len(self._selected_history_item) == 1:
                consistant_ = self.consistant_compare(
                    list(self._selected_history_item.values())[0], node_item)
                if not consistant_:
                    self.compare_error = True
                    return
            self._selected_history_item.update({node_item['id']: node_item})
        else:
            del self._selected_history_item[node_item['id']]

        if len(self._selected_history_item) > 2:
            del self._selected_history_item[node_item['id']]
            self.check_max_compare = True

        self._refresh = True

    def remove_history_item(self, index):
        with rx.session() as session:
            session.query(ChatRunRecord).filter(
                ChatRunRecord.id == index).delete()
            session.commit()

        del self._selected_history_item[index]

        return ToastProvider.show(
            title="record deleted successfully",
            description="",
            duration=3000,
            status="success"
        )

    def consistant_compare(self, node1: ChatRunRecord, node2: ChatRunRecord):
        ok = True
        if len(eval(node1['chat_result'])) != len(eval(node2['chat_result'])):
            ok = False

        return ok

    @rx.var
    def get_compare_num(self) -> int:
        return min(len(self._selected_history_item), 2)

    _columns_scores: List[list] = []
    _refresh: bool = True

    @rx.var
    def query_history_result(self) -> List[List[dict]]:
        process_data = []
        res = []
        if self._selected_history_item:
            with rx.session() as session:
                num_get = 0
                for _, check_record in self._selected_history_item.items():
                    res = session.query(ChatRunRecord).filter(ChatRunRecord.node_name == check_record.get(
                        'node_name'), ChatRunRecord.time_stamp == check_record.get('time_stamp')).first()
                    if res:
                        selected_dataset_result = eval(res.chat_result)
                        if res.dataset == 'None':
                            input_content = [
                                ""] * len(selected_dataset_result) * res.iteration
                        else:
                            ori_dataset = self.processing_dataset(res.dataset)
                            input_content = [
                                data['input'] for data in ori_dataset for _ in range(res.iteration)]
                        # todo: add input and placeholders info
                        if num_get == 0:
                            process_data = [[{'input': input, 'output': item['output'], 'score': str(
                                item['up_score'])}] for input, item in zip(input_content, selected_dataset_result)]
                            if self._refresh and res:
                                self._columns_scores = [
                                    [item[0]['score']] for item in process_data]
                        else:
                            for index, (input, item) in enumerate(zip(input_content, selected_dataset_result)):
                                process_data[index].append(
                                    {'input': input, 'output': item['output'], 'score': str(item['up_score'])})
                                if self._refresh and res:
                                    self._columns_scores[index].append(
                                        str(item['up_score']))

                        num_get += 1

        if self._refresh and res:
            self._refresh = False

        return process_data

    # def on_mount(self):
    #     pass

    def processing_dataset(self, dataset: str) -> list:
        # {"source": [{"placeholders": {"a": ""}, "input": "", "target": ""}]}
        with rx.session() as session:
            processed_dataset = session.query(Dataset).filter(
                Dataset.dataset_name == dataset).first().dict()
        return eval(processed_dataset['source'])

    def set_manual_score(self, column, index, value):
        self._columns_scores[index][column] = value

    def save_avg(self):
        with rx.session() as session:
            for colunm, (key, check_record) in enumerate(self._selected_history_item.items()):
                obj = session.query(ChatRunRecord).filter(ChatRunRecord.node_name == check_record.get(
                    'node_name'), ChatRunRecord.time_stamp == check_record.get('time_stamp')).first()
                up_chat_result = eval(obj.chat_result)
                for index, up_score in enumerate(self._columns_scores):
                    up_chat_result[index]["up_score"] = up_score[colunm]
                obj.chat_result = str(up_chat_result)
                # session.add(obj)
                session.commit()

        return ToastProvider.show(
            title="score is up to date.",
            description="",
            duration=3000,
            status="success"
        )

    @rx.var
    def compute_avgerage(self) -> list:
        columns_avg = []
        if self._columns_scores:
            num_columns = len(self._columns_scores[0])
            for column in range(num_columns):
                columns_avg.append(round(sum([float(
                    scores[column]) for scores in self._columns_scores]) / len(self._columns_scores), 2))
        return columns_avg

    detail_drawer = False
    _item_index: int = -1

    @rx.var
    def show_detial(self) -> List[Dict[str, List[dict]]]:
        query_content = []
        if self._item_index > -1:
            with rx.session() as session:
                for _, check_record in self._selected_history_item.items():
                    content_item = {}
                    if check_record['dataset'] == 'None':
                        content_item['dataset'] = []
                    else:
                        res = session.query(Dataset).filter(
                            Dataset.username == self.username, Dataset.dataset_name == check_record['dataset']).first()
                        show_index = self._item_index % len(eval(res.source))
                        content_item['dataset'] = [json.dumps(
                            eval(res.source)[show_index], indent=1)]

                    res = session.query(ChatNode).filter(
                        ChatNode.node_name == check_record['node_name'], ChatNode.node_version == check_record['node_version']).first()
                    content_item['prompt'] = [{'role': message['role'], 'align': 'right' if message['role'] ==
                                               'assistant' else 'left', 'content': message['content']} for message in eval(res.prompts)]

                    query_content.append(content_item)
        return query_content

    def show_input(self, item_index):
        self._item_index = item_index
        self.detail_drawer = True

    def drawer_close(self):
        self._item_index = -1
        self.detail_drawer = False
