from ttkbootstrap import Style, Button, Entry, Label, Checkbutton, StringVar, IntVar, Toplevel, Combobox, Separator
from tkinter.messagebox import showinfo
from tkinter.font import Font
from adofaihelper import ADOFAI, ADOFAI_read, AskForPath, SaveAsPath, ADOFAI_print

from os import path, getenv, makedirs
from json import load, dump, loads, dumps
from ctypes import windll

appdata_path = getenv('APPDATA')
if not path.exists(cache_path := path.join(appdata_path, 'ADOFAI_event_remover')):
    makedirs(cache_path)
ps_path = path.join(appdata_path, 'ADOFAI_event_remover\\presets.json')
ev_path = path.join(appdata_path, 'ADOFAI_event_remover\\events.json')
ln_path = path.join(appdata_path, 'ADOFAI_event_remover\\lan.json')

try:
    lans = load(open(ln_path, 'r', encoding='utf-8-sig'))
except:
    lans = {
        "English": {
            "Events": [
                ["Gameplay", ["Set Speed", "Twirl", "Checkpoint", "Set Hitsound", "Play Sound", "Set Planet Orbit", "Paused Beats", "Autoplay Tiles", "Scale Planets"]], 
                ["Track Events", ["Set Track Color", "Set Track Animation", "Recolor Track", "Move Track", "Position Track"]], 
                ["Decoration Events", ["Move Decorations", "Set Text", "Set Object", "Set Default Text"]],
                ["Visual Effects", ["Set Background", "Flash", "Move Camera", "Set Filter", "Hall of Mirrors", "Shake Screen", "Bloom", "Tile Screen", "Scroll Screen", "Set Frame Rate"]],
                ["Modifiers", ["Repeat Events", "Set Conditional Events"]],
                ["Conveniences", ["Editor Comment", "Bookmark"]],
                ["DLC", ["Hold", "Set Hold Sound", "Multi Planet", "FreeRoam Segment", "FreeRoam Twirl", "FreeRoam Remove", "Hide Judgement/Floor Icons", "Timing Window Scale", "Planet Radius Scale"]]
            ]
        },
        "Chinese": {
            "Events": [
                ["玩法", ["设置速度", "旋转", "检查点", "设置打拍音", "播放音效", "设置星球轨道", "暂停节拍", "自动播放格子", "缩放行星"]], 
                ["轨道", ["设置轨道颜色", "设置轨道动画", "重新设置轨道颜色", "移动轨道", "位置轨道"]], 
                ["装饰", ["移动装饰", "设置文本", "设置对象", "设置默认文本"]],
                ["视效", ["设置背景", "闪光", "移动摄像头", "预设滤镜", "镜厅", "振屏", "绽放", "平铺", "卷屏", "设置帧率"]],
                ["调整", ["重复事件", "设置条件事件"]],
                ["易用性", ["编辑器附注", "书签"]],
                ["DLC", ["长按", "设置长按音效", "多星球", "自由移动段落", "自由旋转", "自由移除", "隐藏判定/地图图标", "定时窗口大小", "星球半径大小"]]
            ]
        }
    }
    dump(lans, open(ln_path, 'w', encoding='utf-8-sig'), indent=4, ensure_ascii=False)


default_lan = windll.kernel32.GetSystemDefaultUILanguage()
def get_lan(lan):
    global LOAD_CHART, CHART_PATH_TITLE, PRESETS_TITLE, CUSTOM, EVENT_NAMES, EVENT_TITLES, SAVE_PRESET, RENAME, CONFIRM, NEW_PRESET, SAVED, DELETE_PRESET, REMOVE_EVENTS, SELECT_ALL, DESELECT_ALL, INVERSE_SELECT, DUP
    if lan == 2052: # 简体中文
        CHART_PATH_TITLE = '关卡文件：'
        LOAD_CHART = '打开'
        PRESETS_TITLE = '预设：'
        CUSTOM = '自定义'
        EVENT_NAMES = lans["Chinese"]["Events"]
        EVENT_TITLES = [x[0] for x in EVENT_NAMES]
        SAVE_PRESET = '保存预设'
        RENAME = '重命名'
        CONFIRM = '确认'
        NEW_PRESET = '新建预设'
        SAVED = '保存成功'
        DELETE_PRESET = '删除预设'
        REMOVE_EVENTS = '去除选中事件'
        SELECT_ALL = '全选'
        DESELECT_ALL = '全不选'
        INVERSE_SELECT = '反选'
        DUP = '预设名称重复'
    else: # 英文
        CHART_PATH_TITLE = 'Chart File: '
        LOAD_CHART = 'Open'
        PRESETS_TITLE = 'Presets: '
        CUSTOM = 'Custom'
        EVENT_NAMES = lans["English"]["Events"]
        EVENT_TITLES = [x[0] for x in EVENT_NAMES]
        SAVE_PRESET = 'Save Preset'
        RENAME = 'Rename'
        CONFIRM = 'Confirm'
        NEW_PRESET = 'New Preset'
        SAVED = 'Saved'
        DELETE_PRESET = 'Delete Preset'
        REMOVE_EVENTS = 'Remove Selected Events'
        SELECT_ALL = 'Select All'
        DESELECT_ALL = 'Deselect All'
        INVERSE_SELECT = 'Inverse'
        DUP = 'Duplicated preset name'

get_lan(default_lan)



try:
    presets = load(open(ps_path, 'r', encoding='utf-8-sig'))
except:
    presets = {
        "no effect": ["SetDefaultText", "SetFrameRate", "SetHitsound", "PlaySound", "SetPlanetRotation", "AutoPlayTiles", "ScalePlanets", "ColorTrack", "RecolorTrack", "MoveDecorations", "SetText", "SetObject", "CustomBackground", "Flash", "SetFilter", "HallOfMirrors", "ShakeScreen", "Bloom", "ScreenTile", "ScreenScroll", "RepeatEvents", "SetConditionalEvents"],
        "low effect": ["MoveDecorations", "ShakeScreen", "Bloom", "SetFilter", "Flash", "HallOfMirrors", "ScreenTile", "ScreenScroll", "ScalePlanets", "SetFrameRate"]
    }
    dump(presets, open(ps_path, 'w', encoding='utf-8-sig'), indent=4, ensure_ascii=False)

try:
    events = load(open(ev_path, 'r', encoding='utf-8-sig'))
except:
    events = [
        ["SetSpeed", "Twirl", "Checkpoint", "SetHitsound", "PlaySound", "SetPlanetRotation", "Pause", "AutoPlayTiles", "ScalePlanets"],
        ["ColorTrack", "AnimateTrack", "RecolorTrack", "MoveTrack", "PositionTrack"],
        ["MoveDecorations", "SetText", "SetObject", "SetDefaultText"],
        ["CustomBackground", "Flash", "MoveCamera", "SetFilter", "HallOfMirrors", "ShakeScreen", "Bloom", "ScreenTile", "ScreenScroll", "SetFrameRate"],
        ["RepeatEvents", "SetConditionalEvents"], 
        ["EditorComment", "Bookmark"], 
        ["Hold", "SetHoldSound", "MultiPlanet", "FreeRoam", "FreeRoamTwirl", "FreeRoamRemove", "Hide", "ScaleMargin", "ScaleRadius"]
    ]
    dump(events, open(ev_path, 'w', encoding='utf-8-sig'), indent=4, ensure_ascii=False)

preset_loaded = False
chart_loaded = False

def load_preset(preset_name):
    global event_intvars, event_checkbuttons, preset_loaded
    preset_name = presets_combobox.get()
    preset = presets[preset_name]
    for (i, event_group) in enumerate(events):
        for (j, event) in enumerate(event_group):
            event_intvars[i][j].set(int(event in preset))
            event_checkbuttons[i][j].config(state='normal')
    preset_loaded = True
    for button in [new_preset_button, save_preset_button, rename_preset_button, delete_preset_button, select_all_button, deselect_all_button, inverse_select_button]: 
        button.config(state='normal')
    if chart_loaded & preset_loaded:
        remove_events_button.config(state='normal')

def save_presets():
    dump(presets, open(ps_path, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

def new_preset():
    global presets, presets_combobox, preset, event_intvars
    rename_window = Toplevel(root)
    rename_window.title(NEW_PRESET)
    new_preset_name = 'Custom_Preset_'
    i = 1
    while new_preset_name+str(i) in presets:
        i += 1
    default_name = StringVar()
    default_name.set(new_preset_name+str(i))
    rename = Entry(
        rename_window,
        width=40,
        textvariable=default_name
    )
    def save_new_preset():
        removing = []
        for (i, event_intvars_group) in enumerate(event_intvars):
            for (j, event_intvar) in enumerate(event_intvars_group):
                event_intvar.set(0)
        name = rename.get()
        presets[name] = removing
        presets_combobox['value'] = tuple(presets.keys())
        save_presets()
        preset.set(name)
        rename_window.destroy()
    confirm_button = Button(
        rename_window,
        text=CONFIRM,
        command=save_new_preset
    )
    rename.grid(column=0, row=0)
    confirm_button.grid(column=1, row=0)

def save_preset():
    global presets
    removing = []
    for (i, event_intvars_group) in enumerate(event_intvars):
        for (j, event_intvar) in enumerate(event_intvars_group):
            if event_intvar.get():
                removing.append(events[i][j])
    name = preset.get()
    presets[name] = removing
    presets_combobox['value'] = tuple(presets.keys())
    save_presets()
    showinfo('', SAVED)

def rename_preset():
    global presets, preset, presets_combobox
    rename_window = Toplevel(root)
    rename_window.title(RENAME)
    origin_preset_name = preset.get()
    default_name = StringVar()
    default_name.set(origin_preset_name)
    rename = Entry(
        rename_window,
        width=40,
        textvariable=default_name
    )
    def save_new_preset():
        name = rename.get()
        presets[name] = presets[preset.get()]
        if name in presets and origin_preset_name != name:
            showinfo('', DUP)
            return
        del presets[preset.get()]
        presets_combobox['value'] = tuple(presets.keys())
        save_presets()
        preset.set(name)
        rename_window.destroy()
    confirm_button = Button(
        rename_window,
        text=CONFIRM,
        command=save_new_preset
    )
    rename.grid(column=0, row=0)
    confirm_button.grid(column=1, row=0)

def delete_preset():
    global presets, preset, presets_combobox
    del presets[preset.get()]
    preset.set(list(presets.keys())[0])
    presets_combobox['value'] = tuple(presets.keys())
    save_presets()

def load_chart():
    global chart_path_str, chart_path, chart_loaded
    chart_path_str = AskForPath()
    # chart_path.set(path.split(chart_path_str)[1])
    chart_path.set(chart_path_str)
    chart_loaded = True
    if chart_loaded & preset_loaded:
        remove_events_button.config(state='normal')

def select_all():
    global event_intvars
    for event_intvar_group in event_intvars:
        for event_intvar in event_intvar_group:
            event_intvar.set(1)

def deselect_all():
    global event_intvars
    for event_intvar_group in event_intvars:
        for event_intvar in event_intvar_group:
            event_intvar.set(0)

def inverse_select():
    global event_intvars
    for event_intvar_group in event_intvars:
        for event_intvar in event_intvar_group:
            event_intvar.set(event_intvar.get()^1)

def remove_events():
    chart_path = chart_path_present.get()
    contents = ADOFAI_read(chart_path)
    actions=[]
    for action in contents["actions"]:
        if action["eventType"]!=event:
            actions.append(action)
    contents["actions"]=actions
    ADOFAI_print(contents, SaveAsPath(), False)

def reset_text(widgets, new_texts):
    n=len(widgets)
    for i in range(n):
        widget=widgets[i]
        new_text=new_texts[i]
        widget.config(text=new_text)

def refresh(a):
    global default_lan
    landic = {
        '简体中文': 2052, 
        'English': 0
    }
    new_lan = landic[language_combobox.get()]
    if new_lan == default_lan: 
        return
    else:
        default_lan = new_lan
        get_lan(default_lan)
        widgets=[chart_path_title, load_chart_button, presets_title,
                 new_preset_button, save_preset_button, rename_preset_button, delete_preset_button,
                 select_all_button, deselect_all_button, inverse_select_button,
                 remove_events_button
                 ]
        new_texts=[CHART_PATH_TITLE, LOAD_CHART, PRESETS_TITLE,
                   NEW_PRESET, SAVE_PRESET, RENAME, DELETE_PRESET, 
                   SELECT_ALL, DESELECT_ALL, INVERSE_SELECT,
                   REMOVE_EVENTS
                   ]
        reset_text(widgets, new_texts)
        
        for (i, event_title_label) in enumerate(event_title_labels):
            event_title_label.config(text=EVENT_TITLES[i])
        for (i, event_checkbuttons_group) in enumerate(event_checkbuttons):
            for (j, event_checkbutton) in enumerate(event_checkbuttons_group):
                event_checkbutton.config(text=EVENT_NAMES[i][1][j])
        

        

# ROOT WINDOW
style = Style(theme='minty')
# ['cyborg', 'journal', 'darkly', 'flatly', 'solar', 'minty', 'litera', 'united', 'pulse', 'cosmo', 'lumen', 'yeti', 'sandstone']
root = style.master
windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor/75)
root.geometry('2400x1280')
root.resizable(0, 0)
root.title('ADOFAI Event Remover')


# WIDGETS
chart_path_title = Label(
    root,
    text=CHART_PATH_TITLE
)

chart_path_str = ''
chart_path = StringVar()
chart_path.set(chart_path_str)
chart_path_present = Entry(
    root,
    textvariable=chart_path,
    width=93,
    state="disabled"
)

load_chart_button = Button(
    root, 
    text=LOAD_CHART,
    command=load_chart
)

separator_1 = Separator(
    root, 
    orient='horizontal',
)

presets_title = Label(
    root,
    text=PRESETS_TITLE
)

preset = StringVar()
preset.set('')
presets_combobox = Combobox(
    root,
    textvariable=preset
)
presets_combobox['value'] = tuple(presets.keys())
presets_combobox.bind('<<ComboboxSelected>>', load_preset)

event_title_labels = []
for event_title in EVENT_TITLES:
    event_title_labels.append(
        Label(
            root,
            text=event_title,
            font=('Exo', 10, 'bold')
        )
    )

event_intvars = []
for (i, event_group) in enumerate(events):
    event_intvars_group = []
    for (j, event) in enumerate(event_group):
        event_intvars_group.append(
            IntVar(value=0)
        )
    event_intvars.append(event_intvars_group)

event_checkbuttons = []
for (i, event_group) in enumerate(events):
    event_checkbuttons_group = []
    for (j, event) in enumerate(event_group):
        event_checkbuttons_group.append(
            Checkbutton(
                root,
                text=EVENT_NAMES[i][1][j],
                variable=event_intvars[i][j],
                state='disabled'
            )
        )
    event_checkbuttons.append(event_checkbuttons_group)

new_preset_button = Button(
    root,
    text=NEW_PRESET,
    command=new_preset,
    width=11,
    state='disabled'
)

save_preset_button = Button(
    root,
    text=SAVE_PRESET,
    command=save_preset,
    width=11,
    state='disabled'
)

rename_preset_button = Button(
    root,
    text=RENAME,
    command=rename_preset,
    width=11,
    state='disabled'
)

delete_preset_button = Button(
    root, 
    text=DELETE_PRESET,
    command=delete_preset,
    width=11,
    state='disabled'
)

select_all_button = Button(
    root, 
    text=SELECT_ALL,
    command=select_all,
    state='disabled'
)

deselect_all_button = Button(
    root, 
    text=DESELECT_ALL,
    command=deselect_all,
    state='disabled'
)

inverse_select_button = Button(
    root, 
    text=INVERSE_SELECT,
    command=inverse_select,
    state='disabled'
)

remove_events_button = Button(
    root, 
    text=REMOVE_EVENTS,
    command=remove_events,
    state='disabled'
)

language_combobox = Combobox(root)
language_combobox['value'] = ('简体中文', 'English')
if default_lan == 2052: 
    language_combobox.current(0)
else: 
    language_combobox.current(1)
language_combobox.bind('<<ComboboxSelected>>', refresh)


# PLACING
chart_path_title.place(x=520, y=60, anchor='e')
chart_path_present.place(x=1840, y=60, anchor='e')
load_chart_button.place(x=1860, y=60, anchor='w')

separator_1.pack(padx=30, pady=120, fill='x')
presets_title.place(x=800, y=180, anchor='e')
presets_combobox.place(x=820, y=180, anchor='w')

x = 60
for (i, event_checkbuttons_group) in enumerate(event_checkbuttons):
    y = 280
    event_title_labels[i].place(x=x+30, y=y, anchor='w')
    y += 60
    for (j, event_checkbutton) in enumerate(event_checkbuttons_group):
        event_checkbutton.place(x=x, y=y, anchor='w')
        y += 60
    x += 320

new_preset_button.place(x=1260, y=180, anchor='w')
save_preset_button.place(x=1450, y=180, anchor='w')
rename_preset_button.place(x=1640, y=180, anchor='w')
delete_preset_button.place(x=1830, y=180, anchor='w')

select_all_button.place(x=1000, y=1000, anchor='c')
deselect_all_button.place(x=1200, y=1000, anchor='c')
inverse_select_button.place(x=1400, y=1000, anchor='c')

remove_events_button.place(x=1200, y=1100, anchor='c')
language_combobox.place(x=1200, y=1200, anchor='c')

root.mainloop()
