import openpyxl
import csv, json
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm ,AnnotationForm
import random
from .models import DataEntry, Annotation, HighlightedText
from django.contrib.auth.decorators import login_required
################################### File route and Upload #######################


def handle_uploaded_file(file):
   
    data = []
    
    if file.name.endswith('.csv'):
        # Process CSV file
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row[0])  # Assuming the first column contains the title
    elif file.name.endswith('.xlsx'):
        # Process XLSX file
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skipping the header row
            data.append(row[0])  # Assuming the first column contains the title
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or XLSX file.")
    
    return data

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get uploaded file
            file = request.FILES['file']

            try:
                # Process the file to extract titles
                titles = handle_uploaded_file(file)

                # Save each title to the DataEntry model
                for title in titles:
                    DataEntry.objects.create(title=title)  # Add other fields as necessary

                return redirect('home')  # Redirect to a success page
            except ValueError as e:
                return render(request, 'upload.html', {'form': form, 'error': str(e)})

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

################################# User Anotate Form ##################################


# def create_annotation(request):
#     if request.method == 'POST':
#         print("works")
#         form = AnnotationForm(request.POST)
#         print(form)
#         if form.is_valid():
#             annotation = form.save(commit=False)  # Don't save to the database yet
#             annotation.user = request.user  # Set the logged-in user
#             annotation.save()  # Now save to the database
#             return redirect('annotation-list')  # Redirect to some page, e.g., annotation list
#     else:
#         form = AnnotationForm()

#     return render(request, 'create_annotation.html', {'form': form})




@login_required
def random_titles_view(request):
    all_titles = DataEntry.objects.all()
    random_titles = random.sample(list(all_titles), min(20, len(all_titles)))

    if request.method == 'POST':
        selected_titles = request.POST.getlist('title[]')
        annotations = request.POST.getlist('annotate[]')
        highlighted_texts = request.POST.getlist('selected_text[]')  # Extract highlighted text
        # print("after selected text")
        for title_id, annotate in zip(selected_titles, annotations):
            annotation = Annotation(
                title_id=title_id,
                user=request.user,
                annotate=int(annotate)
            )
            annotation.save()
        
       

        # Process highlighted texts
        for highlighted in highlighted_texts:
            try:
                highlight_data = json.loads(highlighted)  # Convert JSON string back to dict
                
                title_id = highlight_data.get("title_id")
                text = highlight_data.get("text")
                # print("text",type(title_id))

                # Save highlighted text (if you have a model for storing highlights)
                HighlightedText.objects.create(
                    title_id=title_id,
                    user=request.user,
                    text=text
                )
                #print(f"Highlighted Text Saved: {text} for Title ID {title_id}")

            except json.JSONDecodeError:
                print("Error decoding highlighted text JSON")

        return redirect('random-titles')

    context = {'titles': random_titles}
    return render(request, 'create_annotation.html', context)


# ####################### csv format###################

def download(request):
    queryset = Annotation.objects.all().values()
    newsSet = DataEntry.objects.all().values()
    selectedText = HighlightedText.objects.all().values()  # Fetch highlighted text

    # print("query", queryset, newsSet, selectedText)

    data = pd.DataFrame(queryset)
    selected_data = pd.DataFrame(selectedText)
    
    if 'title_id' not in data.columns:
        return HttpResponse("The 'title_id' field does not exist in the Annotation data.", status=400)

    news_data = pd.DataFrame(newsSet)

    if 'id' not in news_data.columns or 'title' not in news_data.columns:
        return HttpResponse("The 'id' or 'title' field does not exist in DataEntry data.", status=400)

    # Merge annotations with news titles
    merged_data = pd.merge(data, news_data, left_on='title_id', right_on='id', how='left')

    if merged_data.empty:
        return HttpResponse("No matching titles found for the given 'title_id'.", status=404)

    # Merge selected (highlighted) text with existing data
    if not selected_data.empty and 'title_id' in selected_data.columns:
        merged_data = pd.merge(merged_data, selected_data, on='title_id', how='left')

    grouped_data = merged_data.groupby('title_id').apply(lambda x: x).reset_index(drop=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="grouped_data.csv"'

    grouped_data.to_csv(response, index=False)

    return response
