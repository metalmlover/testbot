# NOTE qna maker is now classic, now we can use Question Answering feature as part of language services
   # First we need to enable and setup the service https://azure.microsoft.com/en-us/services/cognitive-services/question-answering/#overview
   # then we can start using the feature on top of the language service at https://language.azure.com/ 

# for the classic qna maker visit https://www.qnamaker.ai/ and find a link to install the qna service. we can build the qna model if the service is installed refresh the qnamaker.ai page to sense it and appear in step 2 form for creating the knowledge base
# the knowledge base can be edited anytime and more qa pairs can be added
# publish the knowledge base on the site to see deployment settings that are always accesible in the service settings
# the botbuilder.ai package is needed here

from botbuilder.core import TurnContext,ActivityHandler,MessageFactory
from botbuilder.ai.qna import QnAMaker,QnAMakerEndpoint


class QnaBot(ActivityHandler):
   def __init__(self):
      #  arguments are knowledgebase id, endpoint key and host
      # the id is in the link POST /knowledgebases/635d2d04-fd3a-49db-b294-015e3abf00f1/generateAnswer
      # end point key from Authorization: EndpointKey 6cdd055a-f8aa-4638-83ed-0af8c279042a
      # host where our server is running Host: https://qna-test22222.azurewebsites.net/qnamaker
      # note that unexpected errors may occur when the wrong service is used for qna
      qna_endpoint = QnAMakerEndpoint(
            knowledge_base_id='635d2d04-fd3a-49db-b294-015e3abf00f1',
            endpoint_key='6cdd055a-f8aa-4638-83ed-0af8c279042a',
            host="https://qna-test22222.azurewebsites.net/qnamaker",
            )
      self.qna_maker = QnAMaker(qna_endpoint)

   async def on_message_activity(self,turn_context:TurnContext):
      #  response from server
      response = await self.qna_maker.get_answers(turn_context)
      print(response)
      # if there is response and data
      if response and len(response) > 0:
         # returning the first result's answer to user
         await turn_context.send_activity(MessageFactory.text(response[0].answer))
      else:
         await turn_context.send_activity("No QnA Maker answers were found.")