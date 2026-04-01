import unicodedata
import google.generativeai as genai

#テンプレート・指示まとめ
MAIN_TEMPLATES = """
# Instruction
これはダミーテキストです。

# RULES for each section
-企業からのメッセージ
【企業からのメッセージは最大○○文字】
【企業からのメッセージは最大○○文字】
【企業からのメッセージは最大○○文字】

-仕事内容
【仕事内容は最大○○文字】
【仕事内容は最大○○文字】
【仕事内容は最大○○文字】

-AP 
【アピールポイントは最大○○文字】
【アピールポイントは最大○○文字】
【アピールポイントは最大○○文字】
"""

GUIDELINES = """
# 求人原稿基本ルール
これはダミーテキストです。
これはダミーテキストです。
これはダミーテキストです。
"""

CATCHPHRASE_EXAMPLES = """
# キャッチコピーの作成例を挿入する
これはダミーテキストです。
これはダミーテキストです。
これはダミーテキストです。

## サンプルセット
これはダミーテキストです。
"""

DRAFT_BASE_PROMPT =  f"""
これはダミーテキストです。
これはダミーテキストです。

出力指定のイメージ：
これはダミーテキストです。
これはダミーテキストです。

#　出力整形・レイアウトの厳格なルールを規定
これはダミーテキストです。
これはダミーテキストです。
"""

#原稿を作成する際にユーザー側が選択できるポイントをリスト化
APPEAL_POINTS = [
    '【評価・人事】ダミー',
    '【勤務地・転勤】ダミー',
    '【残業・労働時間】ダミー',
    '【オフィス環境】ダミー',
    '【WLB】ダミー',
    '【スキル・キャリア】ダミー',
    '【新規事業・挑戦】ダミー',
    '【社風・裁量権】ダミー',
    '【知名度】ダミー',
    '【教育・研修制度】ダミー',
    '【福利厚生・待遇】ダミー',
]

#ここにはディクショナリーとして最終の整形の際に置き換える文言を包括的にまとめている。
UNIFICATION_MAP = {
    "弊社": "当社",
    "WEB": "Web",
    "ZOOM": "Zoom",
}

#ストリングを最終的に整形関数に繋げるためのスタートライン
#流れ：プロンプト→ドラフト→整形
def build_catchphrase_prompt(interview_log, company_info):
    return f"{CATCHPHRASE_EXAMPLES}\n# 取材情報\n{interview_log}\n# 企業情報\n{company_info}\n指示:これはダミーテキストです。"

def build_manuscript_prompt(interview_log, company_info, template_instructions, sample_message, catch_text, appeal_points):
    ap_instructions = "\n".join([f"■ {r["選択したもの"]}\n指示: {r["加えたい指示"]}" for r in appeal_points]) if appeal_points else "指示なし"
    return f"""
・これはダミーテキストです:{DRAFT_BASE_PROMPT}
・これはダミーテキストです:{GUIDELINES}
・これはダミーテキストです:{interview_log}
・これはダミーテキストです:{company_info}
・これはダミーテキストです:{template_instructions}
・これはダミーテキストです:{sample_message}
・これはダミーテキストです:{catch_text}
・これはダミーテキストです:{ap_instructions}
"""

# モデルが生成した結果を最終的にここに持ってくる→フロントへ表示
# 引数cはクレンジングを意味するために設定
def unify_text(c):
    if not c: 
       return c
    c = unicodedata.normalize("NFKC", c)
    for ng, ok in UNIFICATION_MAP.items():
        c = c.replace(ng, ok)
    return c

def call_generate(interview_log, company_info, template_instructions, sample_message, appeal_points, catch_temp, body_temp):
    model = genai.GenerativeModel('gemini-2.5-flash')
   
    catch_prompt = build_catchphrase_prompt(interview_log, company_info)
    draft_catch = model.generate_content(catch_prompt, generation_config=genai.types.GenerationConfig(temperature=catch_temp))
   
    body_prompt = build_manuscript_prompt(interview_log, company_info, template_instructions, sample_message, draft_catch.text, appeal_points)
    draft_body = model.generate_content(body_prompt, generation_config=genai.types.GenerationConfig(temperature=body_temp, max_output_tokens=20000))
   
    final_body = unify_text(draft_body.text)
    return final_body
