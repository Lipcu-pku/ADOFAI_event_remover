import json, os, time

path=input('请输入adofai文件路径: ').strip('\"')

cor={
    ', }': '}',
    ',  }': '}',
    ']\n\t"decorations"': '],\n\t"decorations"',
    '],\n}': ']\n}',
    ',,': ',',
    '}\n\t\t{':'},\n\t\t{',
    '},\n\t]':'\}\n\t]'
}

with open(path,encoding="utf-8-sig") as f:
    info=f.read()
    for i in cor: info=info.replace(i,cor[i])
    contents=json.loads(info)



def output(contents,suffix):
    fpath, fname = os.path.split(path)
    path_new=fpath+'/'+fname.rstrip('.adofai')+f'({suffix}).adofai'
    contents_new=json.dumps(contents)
    f=open(path_new,'w',encoding='utf-8')
    print(contents_new,file=f)
    f.close()
    return path_new

Track={"ColorTrack", "RecolorTrack", "AnimateTrack", "MoveTrack", "PositionTrack"}
Decoration={"AddDecoration", "MoveDecorations"}
VFX={"AddDecoration", "MoveDecorations", "ShakeScreen", "Bloom", "SetFilter", "Flash", "HallOfMirrors", "ScreenTile", "ScreenScroll"}
Filter={"CustomBackground", "Bloom", "SetFilter", "Flash", "HallOfMirrors", "ScreenTile", "ScreenScroll"}
DLC={"Hold", "SetHoldSound", "MultiPlanet", "FreeRoam", "FreeRoamTwirl", "FreeRoamRemove", "Hide", "ScaleMargin", "ScaleRadius"}
All_events={"SetSpeed", "Twirl", "Checkpoint", "SetHitsound", "PlaySound", "SetPlanetRotation", "Pause", "AutoPlayTiles", "ScalePlanets", 
            "ColorTrack", "AnimateTrack", "RecolorTrack", "MoveTrack", "PositionTrack", 
            "MoveDecorations", "SetText", "SetObject", 
            "CustomBackground", "Flash", "MoveCamera", "SetFilter", "HallOfMirror", "ShakeScreen", "Bloom", "ScreenTile", "ScreenScroll", "SetFrameRate",
            "RepeatEvents", "SetConditionalEvents", 
            "EditorComment", "Bookmark", 
            "Hold", "SetHoldSound", "MultiPlanet", "FreeRoam", "FreeRoamTwirl", "FreeRoamRemove", "Hide", "ScaleMargin", "ScaleRadius"}
Effects={"SetHitsound", "PlaySound", "SetPlanetRotation", "AutoPlayTiles", "ScalePlanets", "ColorTrack", "AnimateTrack", "RecolorTrack", "MoveTrack", "PositionTrack", "MoveDecorations", "SetText", "SetObject", "CustomBackground", "Flash", "MoveCamera", "SetFilter", "HallOfMirror", "ShakeScreen", "Bloom", "ScreenTile", "ScreenScroll", "RepeatEvents", "SetConditionalEvents", "EditorComment", "Bookmark"}
Play_Effect={"SetSpeed", "Twirl", "Checkpoint", "Pause", "Hold", "MultiPlanet", "FreeRoam"}
Replacable={"Hold", "FreeRoam"}

instruction='''请选择要进行的操作: 
1. 删除所有特效（只保留变速、旋转、暂停节拍、长按、自动方块等基础设定）
2. 删除所有高级特效（在基础设定上保留轨道特效与运镜）
3. 删除所有装饰特效（删除所有装饰及其相关事件）
4. 删除所有滤镜（删除滤镜、镜厅、绽放等事件）
5. 删除所有轨道事件（包括位置轨道、移动轨道、颜色轨道等）
6. 删除所有DLC内容（但不影响游玩）
7. 删除单个轨道上的重复事件
8. 删除指定事件
9. 退出程序'''

events='''各事件名如下：
SetSpeed: 设置变速\t\tTwirl: 旋转\t\t\tCheckpoint: 检查点
SetHitsound: 设置打击音\t\tPlaysound: 设置效果音\t\tSetPlanetRotation: 设置星球缓速
Pause: 暂停节拍\t\t\tAutoPlayTiles: 自动方块\t\tScalePlanets: 设置星球大小
ColorTrack: 设置轨道颜色\tAnimateTrack: 轨道动画\t\tRecolorTrack: 重设轨道颜色
MoveTrack: 移动轨道\t\tPositionTrack: 移动轨道
MoveDecorations: 移动装饰\tSetText: 设置文字\t\tSetObject: 设置对象
CustomBackground: 设置背景\tFlash: 闪光\t\t\tMoveCamera: 移动摄像头
SetFilter: 设置滤镜\t\tHallOfMirror: 镜厅\t\tShakeScreen: 振屏
Bloom: 绽放\t\t\tScreenTile: 平铺\t\tScreenScroll: 卷屏
SetFrameRate: 设置帧率
RepeatEvents: 重复事件\t\tSetConditionalEvents: 设置条件事件
EditorComment: 注释\t\tBookmark: 书签
Hold: 长按\t\t\tSetHoldSound: 设置长按音效\tMultiPlanet: 多星球
FreeRoam: 自由阶段\t\tFreeRoamTwirl: 自由阶段旋转\tFreeRoamRemove: 自由阶段挖空
Hide: 隐藏事件图标\t\tScaleMargin: 设置判定窗口\tScaleRadius: 设置轨道半径
All: 所有事件\t\t\tExit: 退出'''

def event_count(event):
    count=0
    for action in contents["actions"]:
        if action["eventType"]==event:
            count+=1
    return count

def remove_all(event):
    actions=[]
    for action in contents["actions"]:
        if action["eventType"]!=event:
            actions.append(action)
    contents["actions"]=actions
    return contents

def remove_deco():
    print(f'共有装饰{len(contents["decorations"])}个')
    contents["decorations"]=[]
    return contents

def remove_dup(event):
    actions=[]
    if event=="SetSpeed":
        existed_floors=set()
        for action in contents["actions"]:
            if action["eventType"]!=event:
                actions.append(action)
            elif action["floor"] not in existed_floors:
                actions.append(action)
                existed_floors.add(action["floor"])
    elif event=="All":
        existed_actions=set()
        for action in contents["actions"]:
            if action not in existed_actions:
                actions.append(action)
                existed_actions.add(action)
    else:
        existed_actions=set()
        for action in contents["actions"]:
            if action["eventType"]!=event:
                actions.append(action)
            elif action not in existed_actions:
                actions.append(action)
                existed_actions.add(action)
    contents["actions"]=actions
    return contents

def event_replace(event):
    actions=[]
    for action in contents["actions"]:
        if action["eventType"]=="Hold" and event=="Hold":
            actions.append({"floor":action["floor"],"eventType":"Pause","duration":2*action["duration"],"countdownTicks":0,"angleCorrectionDir":-1})
        elif action["eventType"]=="FreeRoam" and event=="FreeRoam":
            actions.append({"floor":action["floor"],"eventType":"Pause","duration":action["duration"],"countdownTicks":0,"angleCorrectionDir":-1})
        else:
            actions.append(action)
    contents["actions"]=actions
    return contents

def no_dlc():
    for event in DLC:
        contents=remove_all(event)
    return contents

def MultiPlanets_check():
    for action in contents["actions"]:
        if action["eventType"]=="MultiPlanet":
            if action["planets"]=="ThreePlanets":
                return True
    return False

while True:
    os.system('cls')
    print(f'当前操作文件: {path}')
    print(instruction)
    x=int(input())
    if x==9: 
        break
    elif x==1:
        for event in Effects:
            print(f'共有{event}事件{event_count(event)}个')
            contents=remove_all(event)
        contents=remove_deco()
        path=output(contents,"no effect")
        print(f'已输出到{path}. ')
        break
    elif x==2:
        for event in VFX:
            print(f'共有{event}时间{event_count(event)}个')
            contents=remove_all(event)
        contents=remove_deco()
        path=output(contents,"low effect")
        print(f'已输出到{path}. ')
        break
    elif x==3:
        for event in Decoration:
            print(f'共有{event}事件{event_count(event)}个')
            contents=remove_all(event)
        contents=remove_deco()
        path=output(contents,"no deco")
        print(f'已输出到{path}. ')
    elif x==4:
        for event in Filter:
            print(f'共有{event}事件{event_count(event)}个')
            contents=remove_all(event)
        path=output(contents,"no filter")
        print(f'已输出到{path}. ')
    elif x==5:
        for event in Track:
            print(f'共有{event}事件{event_count(event)}个')
            contents=remove_all(event)
        path=output(contents,"no track effect")
        print(f'已输出到{path}. ')
    elif x==6:
        for event in DLC:
            print(f'共有{event}事件{event_count(event)}个')
            if MultiPlanets_check():
                print('存在三球事件，删除后影响游玩，无法删除！')
                exit()
            contents=remove_all(event)
        path=output(contents,"no dlc")
        print(f'已输出到{path}. ')
    elif x==7:
        removed_dup_events=[]
        while True:
            os.system('cls')
            print(events)
            event=input('请输入想要去除重复的事件(每次只输入一个): ')
            if event=='Exit':
                break
            elif event=="All":
                contents=remove_dup('All')
                break
            elif event not in All_events:
                print(f'{event}事件不存在！请检查拼写后重新输入')
            elif event in removed_dup_events:
                print(f'{event}事件已去除重复，无需再进行')
            else:
                contents=remove_dup(event)
                removed_dup_events.append(event)
        if removed_dup_events==[]:
            break
        suf=', '.join(removed_dup_events)
        path=output(contents,f"removed duplicated {suf}")
        print(f'已输出到{path}. ')
    elif x==8:
        removed_events=[]
        while True:
            comments='' if removed_events==[] else f'已删除{", ".join(removed_events)}' 
            os.system('cls')
            print(comments)
            print(events)
            event=input('请输入想要去除的事件(每次只输入一个): ')
            if event=="Exit":
                break
            elif event=="All":
                print('确定删除所有事件，仅保留原始轨道吗？这大概率会导致关卡无法正常游玩！')
                if input('输入114514继续删除所有事件: ')=='114514':
                    contents["actions"]=[]
                    path=output(contents,"no events")
                    print(f'已输出到{path}. ')
                    time.sleep(1)
                    exit()
            elif event not in All_events:
                print(f'{event}事件不存在！请检查拼写后重新输入')
                time.sleep(1)
            elif event in removed_events:
                print(f'{event}事件已删除，无需删除')
                time.sleep(1)
            elif event_count(event)==0:
                print(f'无{event}事件，无需删除')
                time.sleep(1)
            elif event in Play_Effect:
                print(f'删除{event}事件大概率会导致关卡无法正常游玩，确定要删除吗？')
                if input(f'输入114514继续删除{event}事件: ')=='114514':
                    if event in Replacable:
                        print(f'是否将{event}重写为暂停节拍使得可以正常游玩？')
                        ans=input(f'输入1919810继续删除{event}事件，输入0重写为暂停节拍: ')
                        if ans==0:
                            contents=event_replace(event)
                            path=output(contents,f'replaced {event}')
                        elif ans==1919810:
                            contents=remove_all(event)
                            path=output(contents,f'removed {event}')
                            print(f'已输出到{path}. ')
                            time.sleep(1)
                            break
                    else:
                        contents=remove_all(event)
                        path=output(contents,f'removed{event}')
                        print(f'已输出到{path}. ')
                        time.sleep(1)
                        break
            else:
                print(f'共有{event}事件{event_count(event)}个')
                contents=remove_all(event)
                removed_events.append(event)
                time.sleep(1)
        if removed_events==[]:
            print('未删除事件，返回. ')
            time.sleep(1)
        else:
            suf=', '.join(removed_events)
            path=output(contents, f'removed {suf}')
            print(f'已输出到{path}. ')
            time.sleep(1)
