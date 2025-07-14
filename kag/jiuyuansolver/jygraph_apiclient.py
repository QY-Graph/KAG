import requests
import json
from typing import Dict, Any, Optional
from knext.project import rest
from knext.common.rest import ApiClient


class JygraphClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):

        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def query_project_schema(self, project_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:

        endpoint = '/api/v1/schema/queryProjectSchema'
        url = f'{self.base_url}{endpoint}'
        
        payload = {
            'ProjectId': project_id
        }
        if params:
            payload.update(params)
            
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() 
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP错误发生: {http_err}')
            raise
        except Exception as err:
            print(f'其他错误发生: {err}')
            raise

    def alter_schema(self, request) -> Dict[str, Any]:
        if request:
            body = ApiClient().sanitize_for_serialization(request)

        payload = json.dumps(body)
        endpoint = '/api/v1/schema/alterSchema'
        url = f'{self.base_url}{endpoint}'
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() 
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP错误发生: {http_err}')
            raise
        except Exception as err:
            print(f'其他错误发生: {err}')
            raise

    def query_SpgType(self, name) -> Dict[str, Any]:

        # query_params = []
        # collection_formats = {}
        # if name:
        #     query_params.append(("name", name))
        #     query_params = ApiClient().sanitize_for_serialization(query_params)
        #     query_params = ApiClient().parameters_to_tuples(query_params, collection_formats)

        # payload = json.dumps(query_params)
        endpoint = '/api/v1/schema/querySpgType'
        url = f'{self.base_url}{endpoint}'

        payload = {
            'Name': name
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() 
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP错误发生: {http_err}')
            raise
        except Exception as err:
            print(f'其他错误发生: {err}')
            raise


    def create_project(self, name: str, namespace: str, config: str, desc: str = None, auto_schema=False) -> Dict[str, Any]:

        project_create_request = rest.ProjectCreateRequest(
            name=name, desc=desc, namespace=namespace, config=config, auto_schema=auto_schema
        )
        if project_create_request:
            body = ApiClient().sanitize_for_serialization(project_create_request)
        payload = json.dumps(body)

        endpoint = '/api/v1/project/create'
        url = f'{self.base_url}{endpoint}'
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() 
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP错误发生: {http_err}')
            raise
        except Exception as err:
            print(f'其他错误发生: {err}')
            raise

    def update_project(self, id, config) -> Dict[str, Any]:
        project_create_request = rest.ProjectCreateRequest(id=id, config=config)

        if project_create_request:
            body = ApiClient().sanitize_for_serialization(project_create_request)

        payload = json.dumps(body)
        endpoint = '/api/v1/project/update'
        url = f'{self.base_url}{endpoint}'
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status() 
            return response.content
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP错误发生: {http_err}')
            raise
        except Exception as err:
            print(f'其他错误发生: {err}')
            raise

if __name__ == '__main__':
    BASE_URL = 'http://172.22.162.15:8090' 
    client = JygraphClient(BASE_URL)
    
    try:
        project_id = '1'
        result = client.query_project_schema(project_id)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"查询失败: {e}")    
 