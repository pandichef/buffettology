prompt_suffix_skeptical_boolean_result = """Be skeptical in your response.  
If the final answer is "Yes", then the response must end in the string "Conclusion: Yes".  
If the final answer is "No", then the response must end in the string "Conclusion: No".
Do not use any markdown text in the reponse."""

fisher_prompts = [
    """Does the company have products or services with sufﬁcient market potential to make possible a sizable increase in sales for at least several years?  In this analysis, consider factors like market share, international growth, and cross-selling opportunities?""",
    """Does the management have a determination to continue to develop products or processes that will still further increase total sales potentials when the growth potentials of currently attractive product lines have largely been exploited?""",
    """How effective are the company’s research and development efforts in relation to its size?""",
    """Does the company have an above-average sales organization?""",
    """Does the company have a worthwhile profit margin?""",
    """What is the company doing to maintain or improve profit margins?""",
    """Does the company have outstanding labor and personnel relations?""",
    """Does the company have outstanding executive relations?""",
    """Does the company have depth to its management?""",
    """How good are the company’s cost analysis and accounting controls?""",
    """Are there other aspects of the business, somewhat peculiar to the industry involved, which will give the investor important clues as to how outstanding the company may be in relation to its competition?""",
    """Does the company have a short-range or long-range outlook in regard to profits?""",
    """In the foreseeable future will the growth of the company require sufﬁcient equity ﬁnancing so that the larger number of shares then outstanding will largely cancel the existing stockholders’ beneﬁt from this anticipated growth?""",
    """Does the management talk freely to investors about its affairs when things are going well but “clam up” when troubles and disappointments occur?""",
    """Does the company have a management of unquestionable integrity?""",
]

eps_estimate_y10_prompt = """
For ticker {ticker}, {fisher_prompt0}.  
Use this analysis to estimate the EPS of the company 10 years from now.
Be skeptical in your response.  The response must end in a specific number.
For example, if the EPS in year 10 is 2.999, then the response must end in the 
string "Conclusion: 2.999".  Do not use any markdown text in the reponse and 
do not end the response with a period character.
"""
