from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadFile
from django.contrib import messages
import pandas as pd
# Create your views here.
            
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid(): 
            uploaded_file = request.FILES['file']

            instance = UploadFile(file=uploaded_file) 
            instance.save()
            file_path = instance.file.path
            try:
                if file_path.endswith('.csv'):
                    try:
                        df = pd.read_csv(file_path)
                    except UnicodeDecodeError:
                        df = pd.read_csv(file_path, encoding='ISO-8859-1')
                elif file_path.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                
                else:
                    return render(request, 'upload.html',{
                        'form':form,
                        'error':'Unsupported file format. Please upload a CSV or Excel fiel.'
                    })

                if 'Cust State' not in df. columns or 'DPD' not in df.columns:
                    return render(request, 'upload.html', {
                        'form':form,
                        'erroe':'The file does not containthe the 0required columns: State, DPD'
                    })
                
                summary = df.groupby([' State','DPD']).size().reset_index(name='Count')
                # print(summary.to_html(index=False))
                return render(request , 'result.html',{'summary':summary.to_html(index=False)})
           
            except Exception as e:
                return render(request, 'upload.html',{
                    'form':form,
                    'error':f'Error processing file: {str(e)}'
                })        
        else:
            return render(request,'upload.html',{'from':form,'error':'Invalid form'})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html',{'form':form})