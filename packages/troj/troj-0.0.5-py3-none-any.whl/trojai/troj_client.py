import json
from typing import Optional, Dict, List
from .troj_dataset import TrojDataset
from .utils import assert_valid_name, raise_resp_exception_error, requests_retry


class TrojClient:
    def __init__(
        self,
        *,
        api_endpoint: str = 'https://wct55o2t7c.execute-api.ca-central-1.amazonaws.com/prod/api/v1',
        **kwargs,
    ) -> "Client":
        self._creds_id_token = None
        self._creds_refresh_token = None
        self._creds_api_key = None
        self.api_endpoint = api_endpoint

    def _get_creds_headers(self):
        """
        Get appropriate request headers for the currently set credentials.

        Raises:
            Exception: No credentials set.
        """
        if self._creds_id_token:
            return {"Authorization": f"Bearer {self._creds_id_token}"}
        else:
            raise Exception("No credentials set.")

    # Might want to use access tokens?
    # Access tokens enable clients to securely call APIs protected by identity provider .
    def set_credentials(
        self,
        *,
        id_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        # api_key: Optional[str] = None,
    ):
        """
        Set credentials for the client.

        Args:
            id_token (str, optional): Used by the client to authenticate the user. Defaults to None.
            refresh_token (str, optional): Used to refresh the ID Token. Defaults to None.
            api_key (str, optional): Used to gain access to API
        Raises:
            Exception: Invalid credential combination provided.
        """

        # TODO: Change to require id_token and api_key together
        if id_token is not None:
            self._creds_id_token = id_token
        elif refresh_token is not None:
            self._creds_refresh_token = refresh_token
        # elif api_key is not None:
        #     self._creds_api_key = api_key
        else:
            raise Exception(
                "Please provide either an ID Token, Refresh Token, or API key"
            )

    def test_api_endpoint(self):
        try:
            r = requests_retry.get(
                "https://wct55o2t7c.execute-api.ca-central-1.amazonaws.com/prod/ping"
            )
            return r.status_code
        except Exception as exc:
            raise Exception(f"test_api_endpoint error: {exc}")

    # TODO: Create a project class, then dataset class
    # Users can name projects/datasets hatever they want
    # We store the hashed name in db instead of uuid
    # switch out uuids for names and compare hash in db instead of using uuids
    # profit??

    def create_project(self, project_name: str):
        """
        Create a new project via the REST API.

        Args:
            project_name (str): Name you want to give your project
        """

        assert_valid_name(project_name)

        data = {"project_name": project_name}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects",
            headers=self._get_creds_headers(),
            json=data,
            # data=json.dumps(data),
        )

        if r.status_code == 401:
            #call method to fetch new tokens from cognito.
            self.set_credentials()
            #resend request


        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}
        # if r.status_code == 200:
        #     return f"Project '{project_name}' has been created!"
        # End of create_project()

    def get_projects(self):
        """
        Get data about the users projects
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def project_exists(self, project_name: str):
        """
        Check if a project exists.

        Args:
            project_name (str): Project name

        Returns:
            Dict[int, dict]: dict(data) will either be False or the project itself
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def delete_project(self, project_name: str):
        """
        Try to delete a project

        Args:
            project_name (str): Name of the project to be deleted
        """

        if self.project_exists(project_name)["data"] is False:
            raise Exception(f"Project '{project_name}' does not exist.")

        r = requests_retry.delete(
            f"{self.api_endpoint}/projects/{project_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def create_dataset(
        self,
        project_name: str,
        dataset_name: str,
        dataset: Optional[TrojDataset] = None,
    ):
        assert_valid_name(dataset_name)
        project_data = self.project_exists(project_name)

        data = {
            "project_uuid": project_data["data"]["project_uuid"],
            "dataset_name": dataset_name,
        }

        r = requests_retry.post(
            f"{self.api_endpoint}/datasets",
            headers=self._get_creds_headers(),
            json=data,
            # data=json.dumps(data),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}
        # End of create_dataset()

    def get_project_datasets(self, project_name: str):
        """
        Get info about existing datasets for a specific project

        Args:
            project_name (str): Name of the project you want to find datasets under
        """

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def dataset_exists(self, project_name: str, dataset_name: str):
        """
        Check if a dataset exists.

        Args:
            project_name (str): Project name
            dataset_name (str): Dataset name

        Returns:
            Dict[int, dict]: dict(data) will either be False or the dataset itself
        """
        if self.project_exists(project_name)["data"] is False:
            raise Exception(f"Project '{project_name}' does not exist.")

        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def delete_dataset(self, project_name: str, dataset_name: str):
        if self.dataset_exists(project_name, dataset_name)["data"] is False:
            raise Exception(
                f"Dataset '{dataset_name}' does not exist in project '{project_name}'."
            )

        r = requests_retry.delete(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        return {"status_code": r.status_code, "data": r.json()}

    def upload_df_results(self, project_name: str, dataset_name: str, dataframe: dict):
        """
        Uploads dataframe results to database.

        Args:
            project_name (str): Project name
            dataset_name (str): Dataset name
            dataframe (dict): JSONified dataframe

        Returns:
            Dict[int, bool]: status_code and bool whether success/fail to upload
        """
        try:
            dataset = self.dataset_exists(project_name, dataset_name)["data"]

            if dataset is not False:
                dataset_uuid = dataset["dataset_uuid"]

                r = requests_retry.post(
                    f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/upload_dataframe",
                    json={"dataset_uuid": dataset_uuid, "results": dataframe},
                    headers=self._get_creds_headers(),
                )

                raise_resp_exception_error(r)

                return {"status_code": r.status_code, "data": r.json()}
            else:
                raise Exception(
                    "Something went wrong. Double check the project and dataset names."
                )
        except Exception as exc:
            raise Exception(f"post_dataframe error: {exc}")
