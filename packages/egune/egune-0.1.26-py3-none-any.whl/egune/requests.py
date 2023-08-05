from egune.interfaces import ActorMessage, UserMessage
from typing import Dict, Any, List
from enum import Enum
from datetime import datetime


class ActionServerRequest():
    def __init__(self,
                 request: str,
                 variables: Dict[Any, Any],
                 user_request: Dict[Any, Any] = None,
                 schedule_data: Dict[Any, Any] = {}) -> None:
        self.request = request
        self.variables = variables
        self.user_request = user_request
        self.schedule_data = schedule_data

    def publish(self) -> Dict[Any, Any]:
        return {
            "variables": self.variables,
            "request": self.request,
            "user_message": self.user_request
        }


class ButtonQuestion(ActionServerRequest):
    def __init__(self, question: str, buttons: Dict[str, str], custom_button_request: UserMessage = None):
        v = {
            "question": {
                "text": question,
                "buttons": [name for name in buttons]
            }
        }
        for name in buttons:
            v[name] = buttons[name]  # type:ignore
        super().__init__(
            "ask_button_question",
            v,
            custom_button_request.to_dict() if custom_button_request is not None else None
        )


class YesNoQuestion(ActionServerRequest):
    def __init__(self, question: str, yes_action: str, no_action: str, custom_button_request: UserMessage = None):
        super().__init__(
            "ask_yes_no_question",
            {
                "question": {
                    "text": question
                },
                "yes_action": yes_action,
                "no_action": no_action
            },
            custom_button_request.to_dict() if custom_button_request is not None else None
        )


class OpenQuestion(ActionServerRequest):
    def __init__(self, question: str, handler: str):
        super().__init__(
            "ask_open_question",
            {
                "question": {
                    "text": question
                },
                "answer_handler": handler
            }
        )


class Fail(ActionServerRequest):
    def __init__(self, fail_msg: str = None):
        if fail_msg is None:
            super().__init__(
                "notify_action_fail",
                {"action_text": {"code": "not_understood"}}
            )
        else:
            super().__init__(
                "notify_action_fail",
                {"action_text": {"text": fail_msg}}
            )


class Success(ActionServerRequest):
    def __init__(self, success_msg: str = None):
        if success_msg is None:
            super().__init__(
                "notify_action_fail",
                {"action_text": {"code": "success"}}
            )
        else:
            super().__init__(
                "notify_action_fail",
                {"action_text": {"text": success_msg}}
            )


class Tell(ActionServerRequest):
    def __init__(self, text: str):
        super().__init__(
            "tell_user",
            {"msg": {
                "text": text
            }}
        )


class TellPreparedMessage(ActionServerRequest):
    def __init__(self, msg_code: str):
        super().__init__(
            "tell_user",
            {"msg": {
                "code": msg_code
            }}
        )


class TellCustom(ActionServerRequest):
    def __init__(self,
                 text: str = None,
                 list: List[str] = None,
                 buttons: List[str] = None,
                 checkboxes: List[str] = None,
                 multiselects: List[str] = None,
                 images: List[str] = None,
                 files: List[str] = None):
        super().__init__(
            "tell_user",
            {"msg": ActorMessage(
                text=text,
                list=list,
                buttons=buttons,
                checkboxes=checkboxes,
                multiselects=multiselects,
                images=images,
                files=files
            ).to_dict()}
        )


class Do(ActionServerRequest):
    def __init__(self, action: str, user_request: Dict[Any, Any] = None):
        super().__init__(
            "perform_action",
            {"action": action},
            user_request
        )


class MultiSelectQuestion(ActionServerRequest):
    def __init__(self, question: str, options: List[str], handler: str):
        super().__init__(
            "ask_multi_select_question",
            {
                "answer_handler": handler,
                "question": {
                    "text": question,
                    "multiselects": options
                }
            }
        )


class CheckboxQuestion(ActionServerRequest):
    def __init__(self, question: str, options: List[str], handler: str):
        super().__init__(
            "ask_checkbox_question",
            {
                "answer_handler": handler,
                "question": {
                    "text": question,
                    "checkboxes": options
                }
            }
        )


class DateQuestion(ActionServerRequest):
    def __init__(self, question: str, handler: str):
        super().__init__(
            "ask_open_question",
            {
                "answer_handler": handler,
                "question": {
                    "text": question
                }
            }
        )


class FormQuestionTypes(Enum):
    MultiSelect = 1
    Checkbox = 2
    Open = 3
    Date = 4


class Form(ActionServerRequest):
    def __init__(self, title: str, submit_handler: str):
        super().__init__(
            "ask_form",
            {},
            {"misc": {"form": {
                "submit_handler": submit_handler,
                "questions": []
            }}}
        )
        self.keys = []

    def add_question(self, key: str, type: FormQuestionTypes, question: str, options: List[str] = None):
        if key in self.keys:
            raise ValueError("Question Key Exists")
        else:
            if type == FormQuestionTypes.MultiSelect:
                self.user_request["misc"]["form"]["questions"].append({
                    "key": key,
                    "type": "multi_choice",
                    "question": question,
                    "options": options
                })
            elif type == FormQuestionTypes.Checkbox:
                self.user_request["misc"]["form"]["questions"].append({
                    "key": key,
                    "type": "checkbox",
                    "question": question,
                    "options": options
                })
            elif type == FormQuestionTypes.Open:
                self.user_request["misc"]["form"]["questions"].append({
                    "key": key,
                    "type": "text",
                    "question": question
                })
            elif type == FormQuestionTypes.Date:
                self.user_request["misc"]["form"]["questions"].append({
                    "key": key,
                    "type": "date",
                    "question": question
                })
            else:
                raise ValueError("Invalid Form Question Type")
            self.keys.append(key)


class FormSubmit(ActionServerRequest):
    def __init__(self, submit_handler: str, form_data: Dict[str, Any]):
        super().__init__(
            "submit_form",
            {"endpoint": submit_handler},
            {"misc": {"form": form_data}}
        )
        self.keys = []


class CreateOnTimeEvent:
    def __init__(self,
                 name: str,
                 user_id: str,
                 app_id: str,
                 time: datetime,
                 data: Dict[Any, Any] = {}
                 ):
        self.time = time
        self.user_id = user_id
        self.name = name
        self.data = data
        self.app_id = app_id

    def publish(self):
        return {
            "type": "on-time",
            "user_id": self.user_id,
            "app_id": self.app_id,
            "name": self.name,
            "time": self.time.strftime("%Y-%m-%d, %H:%M:%S"),
            "data": self.data
        }


class CreateWeeklyEvent:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self,
                 name: str,
                 user_id: str,
                 app_id: str,
                 hour: int,
                 minute: int,
                 weekday: int,
                 data: Dict[Any, Any] = {}
                 ):
        self.name = name
        self.user_id = user_id
        self.weekday = weekday
        self.data = data
        self.hour = hour
        self.minute = minute
        self.app_id = app_id

    def publish(self):
        return {
            "type": "weekly",
            "user_id": self.user_id,
            "app_id": self.app_id,
            "hour": self.hour,
            "minute": self.minute,
            "name": self.name,
            "weekday": self.weekday,
            "data": self.data
        }


class CreateMonthlyEvent:
    def __init__(self,
                 name: str,
                 user_id: str,
                 app_id: str,
                 day_of_month: int,
                 hour: int,
                 minute: int,
                 data: Dict[Any, Any] = {}
                 ):
        self.name = name
        self.user_id = user_id
        self.day = day_of_month
        self.data = data
        self.hour = hour
        self.minute = minute
        self.app_id = app_id

    def publish(self):
        return {
            "type": "monthly",
            "user_id": self.user_id,
            "app_id": self.app_id,
            "hour": self.hour,
            "minute": self.minute,
            "name": self.name,
            "day": self.day,
            "data": self.data
        }
