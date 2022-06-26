#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install flask')
get_ipython().system('pip install flask_cors')
# !pip install flask-cors --upgrade


# In[2]:


Data = pd.read_csv("jeju_final.csv")
for i in range(0, len(Data)):
    Data['companyName'][i] = Data['companyName'][i].replace(' ','')
Data


# In[ ]:


Data = Data.reset_index()
Data


# In[ ]:


Data1 = Data[Data["filter"] == 1]
Data1 = Data1.reset_index()
Data1


# In[ ]:


Data2 = Data[Data["filter"] == 2]
Data2


# In[ ]:


Data3 = Data[Data["filter"] == 3]
Data3


# In[ ]:


Data.columns


# In[ ]:


from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import re
import random
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_url_path="/static")
Data = pd.read_csv("jeju_final.csv", encoding="cp949")
for i in range(0, len(Data)):
    Data['companyName'][i] = Data['companyName'][i].replace(' ','')
Data = Data.reset_index()
Data1 = Data[Data["filter"] == 1]
Data1 = Data1.reset_index()
Data2 = Data[Data["filter"] == 2]
Data2 = Data2.reset_index()
Data3 = Data[Data["filter"] == 3]
Data3 = Data3.reset_index()

CORS(app)

Name = Data['companyName']
Tel = Data['tel']
PostcodeDoro = Data['postcodeDoro']
AddressDoro = Data['addressDoro']
AddressJibun = Data['addressJibun']
LatitudeValue = Data['latitude']
LongitudeValue = Data['longitude']
Filter = Data['filter']
FilterNight = Data['filternight']
Filter365 = Data['filter365']

Name1 = Data1['companyName']
AddressDoro1 = Data1['addressDoro']
LatitudeValue1 = Data1['latitude']
LongitudeValue1 = Data1['longitude']

Name2 = Data2['companyName']
AddressDoro2 = Data2['addressDoro']
DetailNight = Data2['filternight']
LatitudeValue2 = Data2['latitude']
LongitudeValue2 = Data2['longitude']

Name3 = Data3['companyName']
AddressDoro3 = Data3['addressDoro']
Detail365 = Data3['filter365']
LatitudeValue3 = Data3['latitude']
LongitudeValue3 = Data3['longitude']

# FLASK API 구현
# FLASK API 생성 예제 1
# jeju-damoa-main.html (http://127.0.0.1:5000/JejuPharmacyMoa)
@app.route("/JejuPharmacyMoa", methods=['GET','POST'])
def MainPage():
    return render_template('jeju-damoa-main.html',
                            len2 = len(Name2),
                            Name2 = Name2,
                            AddressDoro2 = AddressDoro2,
                            DetailNight = DetailNight,
                            len3 = len(Name3),
                            Name3 = Name3,
                            AddressDoro3 = AddressDoro3,
                            Detail365 = Detail365)

# FLASK API 생성 예제 2
# jeju-damoa-detail.html (http://127.0.0.1:5000/PharmacyDetail)
@app.route("/PharmacyDetail", methods=['GET','POST'])
def DetailPage():
    InputName = request.args.get('Name')
    IDX = np.where(Name == InputName)[0]
    return render_template('jeju-damoa-detail.html',
                            Name = Name[IDX].values[0],
                            LatitudeValue=LatitudeValue[IDX].values[0],
                            LongitudeValue=LongitudeValue[IDX].values[0],
                            Tel = Tel[IDX].values[0],
                            AddressDoro = AddressDoro[IDX].values[0],
                            AddressJibun = AddressJibun[IDX].values[0],
                            PostcodeDoro = PostcodeDoro[IDX].values[0],
                            Filter = Filter[IDX])


Data_subarea = pd.read_csv("jeju_final_subarea.csv")
SubArea = Data_subarea['subarea']
SubName = Data_subarea['companyName']
SubTel = Data_subarea['tel']
SubAddressDoro = Data_subarea['addressDoro']

# FLASK API 생성 예제 3
# jeju-damoa-total.html (http://127.0.0.1:5000/JejuPharmacyTotal)
@app.route("/JejuPharmacyTotal", methods=['GET','POST'])
def TotalPage():
    return render_template('jeju-damoa-total.html',
                            len4 = len(SubName),
                            SubArea = SubArea,
                            SubName = SubName,
                            SubTel = SubTel,
                            SubAddressDoro = SubAddressDoro)

# API 작동
app.run(host='localhost', port='5000')


# http://localhost:5000/JejuPharmacyMoa

# http://localhost:5000/PharmacyDetail

# http://127.0.0.1:5000/JejuPharmacyTotal

# ---
# 검색 기능 추가

# In[2]:


# FLASK API 생성 예제 4
# jeju-damoa-total.html (http://127.0.0.1:5000/JejuPharmacyTotal)
@app.route("/JejuPharmacySearch", methods=['GET','POST'])
def TotalPage():
    return render_template('jeju-damoa-total.html',
                            len1 = len(Name1),
                            Name1 = Name1,
                            AddressDoro1 = AddressDoro1,
                            len2 = len(Name2),
                            Name2 = Name2,
                            AddressDoro2 = AddressDoro2,
                            DetailNight = DetailNight,
                            len3 = len(Name3),
                            Name3 = Name3,
                            AddressDoro3 = AddressDoro3,
                            Detail365 = Detail365)

# API 작동
app.run(host='localhost', port='5000')


# http://127.0.0.1:5000/JejuPharmacySearch

# In[2]:


# FLASK API 생성 예제 4
# jeju-damoa-search.html (http://127.0.0.1:5000/JejuPharmacySearch)
@app.route("/JejuPharmacySearch", methods=['GET','POST'])
def TotalPage():
    What = request.args.get('What')
    
    if What == '':
        What_index = [True for i in range(len(Data.set_index('Name')))]
    else:
        What_index = [What in Name or What in AddressDoro or What in AddressJibun for Name, AddressDoro, AddressJibun in zip(Data[Name], Data[AddressDoro], Data[AddressJibun])]

    FinalIndex = pd.Series([What_index])
    return render_template(Name = Name,
                            AddressDoro = AddressDoro,
                            AddressJibun = AddressJibun)

# API 작동
app.run(host='localhost', port='5000')


# In[ ]:


<script>
                                (/, 'request'라는, id를, 가진, 버튼, 클릭, 시, 실행.)
                                What1 = getParam('What')
                                FinalURL = 'http://127.0.0.1:5000/JejuPharmacyTotal?What=' + What1
                                
                                $.ajax({
                                    type : 'GET',
                                    url : 'http://127.0.0.1:5000/JejuPharmacyTotal?What=' + What1,
                                    success : function(result){
                                        var data = JSON.parse(result);
                                        
                                        AddressDoro = Object.values(data.AddressDoro)
                                        Name = Object.values(data.Name)
                                        for (var i=0; i<Data_Category.length; i++){
                                            $("#itemList").append("\
					<div class='grid-item product portrait grid-sizer'>\
						<div class='thumbnail product-thumbnail img-scale-in' data-hover-easing='easeInOut' data-hover-speed='700' data-hover-bkg-color='#000000' data-hover-bkg-opacity='0.5'>\
							<a class='overlay-link' href='#' form method='GET'>\
								<img src='"+images/phbasic.png+"' alt=''>\
								<span class='overlay-info'>\
									<span>\
										<span class='product-title'>"+AddressDoro[i]+"</span>\
									</span>\
								</span>\
							</a>\
						</div>\
						<div class='product-details'>\
							<h3 class='product-title'>\
								<a href='#'><br>"+Name[i]+"</a>\
							</h3>\
							<span class='color-black'> <br> </span>\
						</div>\
					</div>");

                                    }},
                                    error: function(xhr, ajaxOptions, thrownError){
                                    },
                                });
                            </script>

<div class="grid-container fade-in-progressively no-padding-top" data-layout-mode="masonry" data-grid-ratio="1" data-animate-resize data-animate-resize-duration="0" id=""itemList">
</div>


# In[ ]:


<!-- Portfolio Grid -->
							<div class="grid-container fade-in-progressively no-padding-top" data-layout-mode="masonry" data-grid-ratio="1" data-animate-resize data-animate-resize-duration="0">
								<div class="row">
									<div class="column width-12">
										<div class="row grid content-grid-4">
											{% for j in range(0, len2) %}
											<div class="grid-item product portrait grid-sizer">
												<div class="thumbnail product-thumbnail img-scale-in" data-hover-easing="easeInOut" data-hover-speed="700" data-hover-bkg-color="#000000" data-hover-bkg-opacity="0.5">
													<span class="onsale">심야</span>
													<a class="overlay-link" href="{{ url_for('DetailPage', Name=Name2[j]) }}">
														<img src="{{ url_for('static', filename='images/phnight.png')}}" alt=""/>
														<span class="overlay-info">
															<span>
																<span class="product-title">{{AddressDoro2[j]}}</span>
															</span>
														</span>
													</a>
												</div>
												<div class="product-details">
													<h3 class="product-title">
														<a href="{{ url_for('DetailPage', Name=Name2[j]) }}"><br>{{Name2[j]}}</a>
													</h3>
													<span class="color-black">{{DetailNight[j]}}</span>
												</div>
											</div>
											{% endfor %}

											{% for k in range(0, len3) %}
											<div class="grid-item product portrait grid-sizer">
												<div class="thumbnail product-thumbnail img-scale-in" data-hover-easing="easeInOut" data-hover-speed="700" data-hover-bkg-color="#000000" data-hover-bkg-opacity="0.5">
													<span class="onsale">연중무휴</span>
													<a class="overlay-link" href="{{ url_for('DetailPage', Name=Name3[k]) }}">
														<img src="{{ url_for('static', filename='images/phall.png')}}" alt=""/>
														<span class="overlay-info">
															<span>
																<span class="product-title">{{AddressDoro3[k]}}</span>
															</span>
														</span>
													</a>
												</div>
												<div class="product-details">
													<h3 class="product-title">
														<a href="{{ url_for('DetailPage', Name=Name3[k]) }}"><br>{{Name3[k]}}</a>
													</h3>
													<span class="color-black">{{Detail365[k]}}</span>
												</div>
											</div>
											{% endfor %}

											{% for i in range(0, len1) %}
											<div class="grid-item product portrait grid-sizer">
												<div class="thumbnail product-thumbnail img-scale-in" data-hover-easing="easeInOut" data-hover-speed="700" data-hover-bkg-color="#000000" data-hover-bkg-opacity="0.5">
													<a class="overlay-link" href="{{ url_for('DetailPage', Name=Name1[i]) }}">
														<img src="{{ url_for('static', filename='images/phbasic.png')}}" alt=""/>
														<span class="overlay-info">
															<span>
																<span class="product-title">{{AddressDoro1[i]}}</span>
															</span>
														</span>
													</a>
												</div>
												<div class="product-details">
													<h3 class="product-title">
														<a href="{{ url_for('DetailPage', Name=Name3[i]) }}"><br>{{Name1[i]}}</a>
													</h3>
													<span class="color-black"> <br> </span>
												</div>
											</div>
											{% endfor %}
										</div>
										<!-- Portfolio Grid End -->
									</div>
								</div>
							</div>
							<!-- Portfolio Grid End -->

