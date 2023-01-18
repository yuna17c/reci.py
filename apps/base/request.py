import requests
import re
from .models import RecipeList, RecipeGenerator

api_url = "https://recipeland.com/recipes/ingredients/search"
dat = {}
title_lst = []

def create_payload(ing_lst):
    n = 1
    for ing in ing_lst:
        key = "i[i" + str(n) + "]"
        value = ing
        dat[key] = value
        n += 1
    response = requests.post(api_url, data = dat)
    name_lst = find_name(response.text)
    # find_pic(response.text)
    print(name_lst)

# if "Eastern European Kotlety" in response.text:
#     print("success")
text = """<div class="r1" id="recipe_50185">
		<div class="row rlisting" id="rlist_50185">
<div class="col-md-4 recipe-photo">
<a title="Eastern European Kotlety (Meat Patties)" href="https://recipeland.com/recipe/v/eastern-european-kotlety-meat-p-50185">
<picture>
    <source data-srcset="//c.recipeland.com/images/r/13573/eda71a94f99d4d3356c1_400.webp" class="lazyload">
    <source data-srcset="//c.recipeland.com/images/r/13573/eda71a94f99d4d3356c1_400.jpg" class="lazyload">
    <img width="400" height="300" class="img-responsive lazyload" data-src="https://c.recipeland.com/images/r/13573/eda71a94f99d4d3356c1_400.jpg" alt="Eastern European Kotlety (Meat Patties)" /></picture>
</a></div>

<div class="col-md-8"><div class="rbody">
	<h2><a title="Eastern European Kotlety (Meat Patties) recipe" target="_parent" href="https://recipeland.com/recipe/v/eastern-european-kotlety-meat-p-50185">Eastern European Kotlety (Meat Patties)</a></h2>
	<span class="star-rating"><span class="icon-star-filled gold"></span><span class="icon-star-filled gold"></span><span class="icon-star-filled gold"></span><span class="icon-star-empty gold"></span><span class="icon-star-empty gold"></span></span> <sup>(230)</sup>
	<div class="clearfix"></div>
		<small class="r">6 days ago</small>
	<p class="shares" title="# of shares"><span class="icon-share i-24"></span> 394		<img alt="loading..." id="rs_50185" style="display: none" class="" src="https://c.recipeland.com/assets/spin32b-40a7f6dabc6dcd262f3b035cf0b1b4d346e0809cbe2e83042b92ddd783668020.svg" width="32" height="32" />	</p>
	<p>While growing up, my Polish-Russian grandmother, who lived with our family, made these little meat patties quite often and they were a family favorite.  Here is my rendition, fr...</p>
</div>
</div>
</div>

	  </div>
      <div class="r2" id="recipe_52770">
		<div class="row rlisting" id="rlist_52770">
<div class="col-md-4 recipe-photo">
<a title="Grandma&#39;s Best Meatballs, EVER!!!!" href="https://recipeland.com/recipe/v/grandmas-best-meatballs-ever!!!-52770">
<picture>
    <source data-srcset="//c.recipeland.com/images/r/9766/c70fa80fe95f270400cc_400.webp" class="lazyload">
    <source data-srcset="//c.recipeland.com/images/r/9766/c70fa80fe95f270400cc_400.jpg" class="lazyload">
    <img width="400" height="300" class="img-responsive lazyload" data-src="https://c.recipeland.com/images/r/9766/c70fa80fe95f270400cc_400.jpg" alt="Grandma's Best Meatballs, EVER!!!!" /></picture>
</a></div>

<div class="col-md-8"><div class="rbody">
	<h2><a title="Grandma&#39;s Best Meatballs, EVER!!!! recipe" target="_parent" href="https://recipeland.com/recipe/v/grandmas-best-meatballs-ever!!!-52770">Grandma's Best Meatballs, EVER!!!!</a></h2>
	<span class="star-rating"><span class="icon-star-filled gold"></span><span class="icon-star-filled gold"></span><span class="icon-star-filled gold"></span><span class="icon-star-empty gold"></span><span class="icon-star-empty gold"></span></span> <sup>(30)</sup>
	<div class="clearfix"></div>
	<p class="shares" title="# of shares"><span class="icon-share i-24"></span> 214		<img alt="loading..." id="rs_52770" style="display: none" class="" src="https://c.recipeland.com/assets/spin32b-40a7f6dabc6dcd262f3b035cf0b1b4d346e0809cbe2e83042b92ddd783668020.svg" width="32" height="32" />	</p>
	<p>Tasty, moist, delicious, not dense!</p>
</div>
</div>
</div>

	  </div>"""


def find_name(resp):
    regex_name = "<div class=.+recipe-photo.+\n<a title=.+"
    regex_img = "<img .+data-src.+"
    rl_name = re.findall(regex_name, resp)
    rl_img = re.findall(regex_img, resp)
    lst = []
    for i in range(len(rl_name)):
        sstr_name = re.split("\"", rl_name[i])
        name = sstr_name[3]
        link = sstr_name[5]
        sstr_img = re.split("\"", rl_img[i])
        img_link = sstr_img[7]
        if sstr_img[9]!=name:
            img_link = ""
        RecipeList.objects.create(recipe_name=name, link=link, img_link=img_link).save()

    return lst

# find_name(text)
# def find_pic(resp):
#     regex = "<img .+alt"
#     rl = re.findall(regex, resp)
#     # print(rl)
# create_payload(lst)