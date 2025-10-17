#!/usr/bin/python

import json
import urllib.error
import urllib.request
from abc import ABC, abstractmethod

from ansible.module_utils.basic import AnsibleModule, env_fallback

DOCUMENTATION = r"""
---
module: ai
short_description: AI text processing module
description: This module processes text using an AI service.
author:
  - yamause
version_added: "0.0.0"
options:
  text:
    description: The text to process.
    type: str
    required: true
  api_key:
    description: API key for the AI service.
    type: str
    required: false
    no_log: true
  model:
    description: The AI model to use.
    type: str
    required: false
    default: gemini-2.5-flash
"""

EXAMPLES = r"""
---
- name: Test AI Module
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Use custom module to output a value
      yamause.test.ai:
        text: メモリーの使用率についてMarkdown形式でレポートを作成してください。会話は不要です。あなたはAPIのようにレポートの結果だけを出力してください。 {{ memory_info.stdout }}
        api_key: 1234567890 (YOUR_API_KEY_HERE or set via environment variable AI_API_KEY)
        model: gemini-2.5-flash (YOUR_MODEL_HERE or set via environment variable AI_MODEL)
      register: result

    - name: Print the result
      ansible.builtin.debug:
        msg: "{{ result.message }}"
      when: result.message is defined

    - name: Output report
      ansible.builtin.copy:
        content: "{{ result.message }}"
        dest: ai_report.md
        mode: "0644"
      when: result.message is defined
"""


class AiAgent(ABC):
    @abstractmethod
    def process_text(self, text: str) -> str:
        pass


class GeminiAgent(AiAgent):
    def __init__(self, module: AnsibleModule, api_key: str, model="gemini-2.5-flash"):
        self.module = module
        self.api_key = api_key
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def process_text(self, text: str) -> str:
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {"parts": [{"text": text}]}
            ]
        }
        data = json.dumps(payload).encode('utf-8')

        request = urllib.request.Request(
            self.base_url, data=data, headers=headers, method="POST")

        try:
            # リクエストを送信
            with urllib.request.urlopen(request) as response:
                # レスポンスデータを読み込み、JSONとしてパース
                response_body = response.read().decode('utf-8')
                response_json = json.loads(response_body)

                # レスポンスから生成されたテキストを抽出
                if 'candidates' in response_json and len(response_json['candidates']) > 0:
                    generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
                    return generated_text
                else:
                    self.module.fail_json(
                        msg="Gemini API response does not contain candidates.")
                    return None

        except urllib.error.HTTPError as e:
            # HTTPエラー（4xx, 5xxなど）の処理
            self.module.fail_json(
                msg=f"Gemini API returned HTTP error: {e.code} - {e.reason}")

        except urllib.error.URLError as e:
            # その他のURL関連エラーの処理
            self.module.fail_json(msg=f"Gemini API URL error: {e.reason}")

        except Exception as e:
            # その他の一般的なエラーの処理
            self.module.fail_json(
                msg=f"An unexpected error occurred: {str(e)}")


def run_module():
    # モジュールの引数定義

    module_args = {
        "text": {
            "type": "str",
            "required": True
        },
        "api_key": {
            "type": "str",
            "required": False,
            "no_log": True,
            "fallback": (env_fallback, ['AI_API_KEY'])
        },
        "model": {
            "type": "str",
            "required": False,
            "default": "gemini-2.5-flash",
            "fallback": (env_fallback, ['AI_MODEL'])
        }
    }

    # 結果を格納する辞書
    result = {
        "changed": False,
        "message": "",
    }

    # AnsibleModuleオブジェクトの作成
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # 引数から値を取得
    text: str = module.params['text']
    api_key: str = module.params['api_key']
    model: str = module.params['model']

    # AIエージェントのインスタンスを作成
    if model.startswith("gemini-"):
        agent = GeminiAgent(module, api_key, model)
    else:
        module.fail_json(msg=f"Unsupported model: {model}")

    # テキストを処理
    generated_text = agent.process_text(text)

    if generated_text is not None:
        result['message'] = generated_text
    else:
        module.fail_json(
            msg="Failed to process text with AI service.")

    # 結果を返す
    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
