# coding: utf-8
import os
# API tokenをGitHubにあげるな!!!!!!!!
API_TOKEN = os.environ["SLACK_API"]
# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "使い方は `@sortnazonazobot usage` で見れます"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']
