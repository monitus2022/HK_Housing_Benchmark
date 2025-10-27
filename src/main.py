# from cloud_storage import StorageManager
# from evaluations.text_preprocess.text_preprocess import TextPreprocessor
from llm import LocalOllamaConnector
from pprint import pprint
from logger import housing_logger


def main():
    wiki_data = [
            {
                "title": "簡介",
                "text": "由於住宅望向山景及十分寧靜，故發展商把其包裝成豪宅，開售呎價達至約11,000元起。大廈樓高31層，分為2座，共提供153個單位，為一梯三伙，而單位約介乎1500-5300平方呎。另設4座3層高的洋房，每座設有獨立電梯及私家游泳池。而另有3層高的停車場。"
            },
            {
                "title": "歷史",
                "text": "名家匯前身為同是恒基兆業地產的仁安醫院側的露天停車場。到1990年代因醫院營運出現問題，恒基主席李兆基每個月需注資300萬繳付員工薪金，所以到1988年至2000年申請將部份用地改變為住宅用途，最終獲城規會於2000年6月通過建成6座住宅，2004年補地價逾6億元，於2010年2月開售。審計於2012年報告披露該醫院違反批地條款，業主恒基成功向地政總署申請改變土地用途，獲利23億。事件引起公民黨立法會議員郭家麒質疑是否涉及利益輸送。"
            },
            {
                "title": "命名",
                "text": "發展商由於物業可望多個山景（包括獅子山、筆架山、尖山、金山及針山等），故稱為「名家匯」。"
            },
            {
                "title": "會所",
                "text": "物業設有豪華會所「名家會所」Master Club，位在5樓平台上，面積近70,000方呎，其設施包括包括園林泳池及露天風呂按摩池，水療室、運動室、宴會廳、私人影院、卡拉OK房、仿滑雪練習場的滑雪練習機、遊戲室及桌球室等。游泳池旁邊另外設有兒童遊樂專區，更有小型迷宮。"
            },
            {
                "title": "附近住宅",
                "text": "瑞鋒花園\n聚龍居"
            },
            {
                "title": "外部連結",
                "text": "\n名家匯 官方網頁（页面存档备份，存于互联网档案馆）"
            }
        ]
    
    system_messages = """
    你是一個助手，幫助根據提供的數據識別香港住宅物業的相關信息。
    數據結構化為一個部分列表，文本為繁體中文。
    """
    user_messages = f"""
    根據以下關於香港住宅物業的數據：
    {wiki_data}
    識別哪些部分與住宅物業無關。
    不要只根據標題來判斷相關性，還要考慮文本內容。
    以1到10的規模評分各部分的相關性，其中1表示完全無關，10表示高度相關。
    以JSON格式提供答案，作為包含'section'、'relevance_score'和'justification'字段的對象列表。
    """
    
    
    ollama_connector = LocalOllamaConnector()
    ollama_connector.set_model("qwen3:8b")
    response = ollama_connector.generate_response(
        user_messages=user_messages,
        system_messages=system_messages,
        # max_tokens=500,
        temperature=0.7
    )
    response_text = response.get("message", {}).get("content", "") if response else "No response"
    housing_logger.info(f"Response from Ollama: {response_text}")
    

if __name__ == "__main__":
    main()
