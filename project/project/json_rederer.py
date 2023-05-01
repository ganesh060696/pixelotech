from rest_framework import status
from rest_framework.renderers import JSONRenderer


def get_status(code):
    """Get the human-readable SNAKE_CASE version of a status code."""
    for name, val in status.__dict__.items():
        if not callable(val) and code is val:
            return name.replace("HTTP_%s_" % code, "")
    return "UNKNOWN"


class BaseAPIJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Custom API response format for all APIs
        Example success:
        {
            "code": 200,
            "status": "OK",
            "data": {
                "key": "value"
            }
        }

        Example error:
        {
            "code": 404,
            "status": "NOT_FOUND",
            "errors": [
                {
                    "detail": "Not found."
                }
            ]
        }
        """
        response = renderer_context["response"]

        # Modify the response into a cohesive response format
        modified_data = {
            'success': status.is_success(response.status_code)
        }

        if status.is_client_error(response.status_code) or status.is_server_error(
            response.status_code
        ):
            modified_data["errors"] = data

        else:
            if isinstance(data, dict):
                if data.get("results") is not None:
                    modified_data["count"] = data.get("count")
                    modified_data["next"] = data.get("next")
                    modified_data["previous"] = data.get("previous")
                    modified_data["data"] = data.get("results")
                    if data.get("page"):
                        modified_data["page"] = data.get("page")
                else:
                    modified_data["data"] = data
            else:
                modified_data["data"] = data

        return super().render(modified_data, accepted_media_type, renderer_context)


def get_error_message(error_dict):
    response = error_dict[next(iter(error_dict))]
    error_name = next(iter(error_dict))
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]

    return response.replace("This", error_name)


class ApiV3JSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Modify API response format.
        Example success:
        {
            "code": 200,
            "status": "OK",
            "message": "updated successfully",
            "data": {
                "name": "name"
            }
        }

        Example error:
        {
            "code": 404,
            "status": "NOT_FOUND",
            "errors":
                {
                    "error_message": "Selected date cannot be a past date",
                    "error_code": "BAD_REQUEST"
                }
        """
        response = renderer_context["response"]

        # Modify the response into a cohesive response format
        modified_data = {
            "success": status.is_success(response.status_code),
        }

        if status.is_client_error(response.status_code) or status.is_server_error(
            response.status_code
        ):
            error_message = ""
            err_title = ""
            err_dev_message = ""
            if isinstance(data, list) and data:
                if isinstance(data[0], dict):
                    error_message = (get_error_message(data),)
                elif isinstance(data[0], str):
                    error_message = data[0]
            if isinstance(data, dict):

                if data.get("err_title"):
                    err_title = data.get("err_title")

                if data.get("err_dev_message"):
                    err_dev_message = data.get("err_dev_message")

                if data.get("error_message"):
                    error_message = data.get("error_message")
                else:
                    error_message = get_error_message(data)

            error = {
                "err_title": err_title,
                "error_message": error_message,
                "err_dev_message": err_dev_message,
                "error_code": get_status(response.status_code)
            }
            modified_data["errors"] = error

        else:
            modified_data["display_message"] = data.pop("display_message", None)
            modified_data["total_count"] = data.get("total_count")
            modified_data["next"] = data.get("next")
            modified_data["previous"] = data.get("previous")
            modified_data["next_page"] = data.get("next_page")
            modified_data["current_page"] = data.get("current_page")
            modified_data["previous_page"] = data.get("previous_page")
            modified_data["previous_page"] = data.get("previous_page")
            modified_data["page_size"] = data.get("page_size")

            if isinstance(data, dict):
                if data.get("data") is not None:
                    modified_data["data"] = data.get("data")
                else:
                    modified_data["data"] = data
            else:
                modified_data["data"] = data

        return super().render(modified_data, accepted_media_type, renderer_context)
