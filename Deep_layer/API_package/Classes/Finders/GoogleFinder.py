import wikipedia as w
from Deep_layer.API_package.Interfaces import IFinder
from googlesearch import search
class GoogleFinder(IFinder.IFinder):

    @classmethod
    def find(cls, message_text):

        output = []
        outlist = search(message_text, num_results=9, advanced=True, region="ru", lang="ru")

        for outex in outlist:
            output.append(str(outex.title) + ' ' + str(outex.url))
        return set(output)