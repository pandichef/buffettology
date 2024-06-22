from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# from .models import FineTuningJob
# from .oai_queries import get_completion


def script_view(request):
    # if request.method == "POST":
    #     print("====> START")
    #     prompt = request.POST.get("prompt")
    #     response = get_completion(prompt)
    #     print("====> END")
    #     return JsonResponse({"response": response})
    # return render(
    #     request, "query.html", {"update_text": FineTuningJob.get_lastest_update_date()}
    # )
    import os

    def list_files_in_directory(directory_path):
        return os.listdir(directory_path)

    directory_path = "../scripts"
    file_list = list_files_in_directory(directory_path)
    # print(file_list)

    return HttpResponse(
        "CURRENT DILIGENCE STEPS BY PYTHON FILE NAME:<br>" + "<br>".join(file_list)
    )
