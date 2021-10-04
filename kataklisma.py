#!/usr/bin/python

# Katacoda to Instruqt converter


# v. 0.0.2
# Support for bulk migrate with git submodule
#
# v. 0.0.1
# First draft
#

import os
import json
import yaml
import re
import shutil


track_d={}

with open('learn-katacoda//homepage-pathway.json', 'r') as hfile:
    hdata=hfile.read()

hcourses = json.loads(hdata)

for course in hcourses['courses']:
    path=re.match('https\:\/\/learn\.openshift\.com\/(.*)\/', course["external_link"] )
    pathway=path.group(1)
    print("Creating or updating Topic : " + pathway)
    
    if not os.path.exists(pathway):
      os.mkdir(pathway)
      print("Directory " , pathway ,  " Created ")
    else:    
      print("Directory " , pathway ,  " already exists")
  
    print("Reading pathway " + 'learn-katacoda/' + pathway + '-pathway.json')
    with open('learn-katacoda/' + pathway + '-pathway.json', 'r') as myfile:
        data=myfile.read()

    courses = json.loads(data)

    for course in courses['courses']:
        pathway_id=''
        if "pathway_id" in course:
          pathway_id=course['pathway_id']
        else:
          pathway_id=pathway
        
        course_id=course['course_id']
        title=course['title']
        
        trackDir=course_id
        
        
        track_d["title"] = title
        track_d["slug"] = course_id
        track_d["type"] = "truck"
        
        if not os.path.exists(pathway + '/' + trackDir):
          os.mkdir(pathway + '/' + trackDir)
          print("Directory " , pathway + '/' + trackDir ,  " Created ")
        else:    
          print("Directory " , pathway + '/' + trackDir ,  " already exists")
        
        
        try:
          with open('learn-katacoda/' + pathway_id + '/' + course_id + '/index.json', 'r') as mycourse:
              course_data=mycourse.read()
        except FileNotFoundError:
          print("Path " + 'learn-katacoda/' + pathway_id + '/' + course_id + '/index.json' + " not found, skipping")
          continue
        
        course_json = json.loads(course_data)
        
        track_d["icon"] = "https://logodix.com/logo/1910931.png"
        
        track_d["tags"] = ["openshift"]
        track_d["owner"] = ["openshift"]
        track_d["developers"] = [ "btannous@redhat.com", "nvinto@redhat.com","rjarvine@redhat.com"]
        track_d["private"] =  "false"
        track_d["published"] = "true"
        track_d["skipping_enabled"] = "true"
        
        difficulty="intermediate"
        level="beginner"
        # course_json["time"]
        time="300"
        
        if course_json["difficulty"] == "beginner":
          difficulty="basic"
          level="beginner"
        
        track_d["level"] = level
      
            
        l_challenges=[]
        d_challenges={}
        
        src=r'config.yml'
        dst= pathway + '/' + trackDir + '/' + 'config.yml'
        shutil.copyfile(src, dst)
        
        shutil.copytree('track_scripts', pathway + '/' + trackDir + '/track_scripts')
        
        
        for step in course_json["details"]["steps"]:
            slug = step["text"]
            
            slug = re.sub(r'\.md$', '', slug )
            
            if not os.path.exists(pathway + '/' + trackDir + '/' + slug):
              os.mkdir(pathway + '/' + trackDir + '/' + slug)
              print("Directory " , pathway + '/' + trackDir + '/' + slug ,  " Created ")
            else:    
              print("Directory " , pathway + '/' + trackDir + '/' + slug ,  " already exists")
            



            
            
            d_challenges["slug"] = slug
            d_challenges["title"] = step["title"]
            d_challenges["type"] = "challenge"
            
            with open('learn-katacoda/' + pathway_id + '/' + course_id + '/' + step["text"], 'r') as myassign:
                assign_data=myassign.read()
            
            md=re.sub(r'`{1,3}(.+?)`{1,3}\{\{execute\}\}', r'```\n\1\n```', assign_data )
            md=re.sub(r'\{\{copy\}\}',r'', md)
            md=re.sub(r'\(\.\.\/\.\.\/assets',r'(https://katacoda.com/openshift/assets',md)
            
            d_challenges["assignment"] =  md
            
            d_challenges["tabs"] = [{"title": "cli", "type": "terminal","hostname":"crc-nonest-1"},
                                    {"title": "web-ui", "type" : "service", "hostname" : "crc-nonest-1", "port" : "30443"}]
            
            d_challenges["difficulty"]= difficulty
            d_challenges["timelimit"]= time
            
            dictionary_copy = d_challenges. copy()
            l_challenges.append(dictionary_copy);
            


        
        track_d["challenges"] = l_challenges
        
        with open(pathway + '/' + trackDir + '/track.yml', 'w') as yaml_file:
          yaml.dump(track_d, yaml_file, default_flow_style=False)




    

