import reflex as rx
from prompt_go.states import State, Dataset, ChatRunRecord
from typing import List
import json


NULL_DATA = {'dataset_name': 'None', 'description': 'Preset empty dataset',
             'source': "[{'input': '', 'target': ''}]"}


class DatasetState(State):

    data_upload_error: bool = False

    def up_datasset_error(self):
        self.data_upload_error = not self.data_upload_error

    data_upload_done: bool = False

    def up_dataset_done(self):
        self.data_upload_done = False

    input_data_name: str
    upload_dataset_content: str = ''

    def upload_dataset(self, form: dict):
        if self._data_name_exist:
            return

        with rx.session() as session:
            session.add(Dataset(username=self.username,
                        dataset_name=form['dataset_name'], description=form['description'], source=self.upload_dataset_content))
            session.commit()

        self.input_data_name = ''
        self.upload_dataset_content = ''
        self.data_upload_done = True

    async def handle_upload(
        self, files: List[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        upload_data = await files[0].read()
        content = json.loads(upload_data)
        if not isinstance(content, list):
            self.up_datasset_error()
            return

        if not all(isinstance(item, dict) and set(item.keys()) == {'placeholders', 'input', 'target'} and isinstance(item.get('placeholders'), dict) for item in content):
            self.up_datasset_error()
            return

        self.upload_dataset_content = str(content)

        self.input_data_name = files[0].filename.split('.')[0]

    _data_name_exist: bool = False

    @rx.var
    def dataname_exists(self) -> bool:
        with rx.session() as session:
            res = session.query(Dataset).filter(
                Dataset.dataset_name == self.input_data_name).first()
            if res:
                self._data_name_exist = True
                return True

        self._data_name_exist = False
        return False

    @rx.var
    def data_list(self) -> List[dict]:
        pre_data = {'username': self.username, **NULL_DATA}
        with rx.session() as session:
            res = session.query(Dataset).filter(
                Dataset.username == self.username).all()
            return [pre_data] + res

    show_data_drawer: bool = False
    show_data_content: dict = {}

    def show_data(self, dataset_name):
        with rx.session() as session:
            res = session.query(Dataset).filter(
                Dataset.username == self.username, Dataset.dataset_name == dataset_name).first()
            self.show_data_content['content'] = json.dumps(
                eval(res.source), indent=1)
            self.show_data_content['number'] = str(
                len(eval(res.source))) + ' items'
            self.show_data_content['name'] = dataset_name
            self.show_data_content['description'] = res.description
        self.show_data_drawer = True

    def data_drawer_close(self):
        self.show_data_drawer = False

    delete_confirm: bool = False
    _delete_item: dict = {}

    def remove_data(self, item: dict):
        self.delete_confirm = True
        self._delete_item = item

    def del_confirm_status(self, del_flag: bool):
        if del_flag:
            with rx.session() as session:
                # delete associated History Record
                session.query(ChatRunRecord).filter(
                    ChatRunRecord.dataset == self._delete_item['dataset_name']).delete()

                # Delete dataset
                session.query(Dataset).filter(Dataset.dataset_name ==
                                              self._delete_item['dataset_name']).delete()
                session.commit()

        self._delete_item = {}
        self.delete_confirm = False
