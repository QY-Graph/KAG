import requests
import json
from typing import Dict, Any, Optional

class ProjectSchemaClient:
    """项目架构查询API客户端"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            base_url: API基础URL
            api_key: 认证API密钥(如果需要)
        """
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def query_project_schema(self, project_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        查询项目架构
        
        Args:
            project_id: 项目ID
            params: 查询参数
            
        Returns:
            API响应数据
            
        Raises:
            HTTPError: API调用失败
        """
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

if __name__ == '__main__':
    BASE_URL = 'http://172.22.162.15:8090' 
    client = ProjectSchemaClient(BASE_URL)
    
    try:
        project_id = '1'
        result = client.query_project_schema(project_id)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"查询失败: {e}")    