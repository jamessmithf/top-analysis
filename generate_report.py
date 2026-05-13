import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Шрифт ────────────────────────────────────────────────────
for fp, fb in [
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
     '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
]:
    if os.path.exists(fp):
        pdfmetrics.registerFont(TTFont('R',  fp))
        pdfmetrics.registerFont(TTFont('RB', fb))
        break

BASE = '/home/viktor/unix_labs/top_analysis'
os.makedirs(BASE, exist_ok=True)

# ════════════════════════════════════════════════════════════════
# ГРАФІКИ
# ════════════════════════════════════════════════════════════════
plt.rcParams.update({'font.family': 'DejaVu Sans', 'figure.dpi': 150,
                     'axes.spines.top': False, 'axes.spines.right': False})

BLUE   = '#2563EB'; ORANGE = '#F59E0B'; RED = '#EF4444'
GREEN  = '#10B981'; GRAY   = '#94A3B8'; PURPLE = '#7C3AED'
DARK   = '#1E3A5F'; LIGHT  = '#DBEAFE'

# ── Рис 1: Аннотований лістинг top ──────────────────────────
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis('off')
fig.patch.set_facecolor('#0F172A')

listing = [
    "top - 17:25:19 up 104 days, 13:31,  4 users,  load average: 1.10, 1.25, 0.82",
    "Tasks: 254 total,   5 running, 243 sleeping,   0 stopped,   6 zombie",
    "Cpu(s): 52.3%us, 17.7%sy,  0.0%ni, 10.2%id, 19.8%wa,  0.0%hi,  0.0%si",
    "Mem:   4147268k total,  3971588k used,   175680k free,   236316k buffers",
    "Swap:  4096532k total,     1984k used,  4094548k free,  1634360k cached",
    "",
    "  PID USER      PR  NI  VIRT   RES  SHR S %CPU %MEM    TIME+   COMMAND",
    " 1722 mysql     15   0  645m  176m 4336 S 34.5  4.4 260:28.94 mysqld",
    "29790 32023     16   0     0     0    0 Z 15.9  0.0   0:00.48 php <defunct>",
    "29791 32023     16   0     0     0    0 Z 15.9  0.0   0:00.48 php <defunct>",
    "29787 32748     16   0     0     0    0 Z 13.6  0.0   0:00.41 php <defunct>",
    "29784 32333     17   0     0     0    0 Z  9.6  0.0   0:00.29 php <defunct>",
    "29807 33557     18   0 30712   17m 4480 R  7.6  0.4   0:00.23 php",
    "29804 32489     16   0 25492   11m 4748 S  4.6  0.3   0:00.14 php",
    " 21958 root     16   0  9548  6056 1068 S  3.3  0.1 667:20.38 psmon",
    "29808 32649     17   0     0     0    0 Z  3.0  0.0   0:00.09 php <defunct>",
    " 17989 root     16   0 13056  6120 1136 S  1.7  0.1 689:09.00 psmon",
]

row_colors = {
    0: '#1E3A5F', 1: '#1E3A5F', 2: '#1E3A5F', 3: '#1E3A5F', 4: '#1E3A5F',
    6: '#334155',
    7: '#3B1F00',   # mysql - помаранчевий відтінок
    8: '#3B0000', 9: '#3B0000', 10: '#3B0000', 11: '#3B0000',  # zombie
    15: '#3B0000',  # zombie
    14: '#1E293B', 16: '#1E293B',  # psmon
}

y_start = 9.5
row_h   = 0.52
for i, line in enumerate(listing):
    y = y_start - i * row_h
    bg = row_colors.get(i, '#1E293B')
    rect = FancyBboxPatch((0.05, y - 0.38), 15.9, row_h - 0.04,
                          boxstyle='round,pad=0.02',
                          facecolor=bg, edgecolor='none')
    ax.add_patch(rect)
    col = '#94A3B8' if line == '' else '#E2E8F0'
    ax.text(0.2, y - 0.1, line, fontsize=7.2, color=col,
            fontfamily='monospace', va='center')

# Аннотації — стрілки
arrow_kw = dict(arrowstyle='->', color='#FCD34D', lw=1.3,
                connectionstyle='arc3,rad=0')
txt_kw   = dict(fontsize=7.5, color='#FCD34D', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E3A5F',
                          edgecolor='#FCD34D', linewidth=0.8))

annotations = [
    # (text, xy_arrow, xytext)
    ('Поточний час',        (1.35, 9.50), (0.1, 8.8)),
    ('Аптайм: 104 дні',     (3.60, 9.50), (3.5, 8.8)),
    ('Активних юзерів: 4',  (6.80, 9.50), (7.2, 8.8)),
    ('Load avg: 1.10/1.25/0.82', (11.5, 9.50), (11.0, 8.8)),
    ('6 ZOMBIE-процесів!',  (10.8, 8.98), (13.5, 8.3)),
    ('CPU user-space: 52.3%',(2.2,  8.46), (0.1,  7.7)),
    ('I/O Wait: 19.8%  [!]',(7.5,  8.46), (9.8,  7.7)),
    ('Idle лише 10.2%',     (5.5,  8.46), (5.3,  7.7)),
    ('RAM: 95.7% зайнято!', (5.5,  7.93), (5.3,  7.0)),
    ('Swap майже вільний',  (5.5,  7.40), (6.5,  6.6)),
    ('MySQL: 34.5% CPU',    (5.0,  5.83), (0.1,  5.1)),
    ('Z = Zombie (defunct)',(8.5,  5.30), (11.5, 4.6)),
    ('psmon: 667год CPU!',  (8.5,  4.24), (11.5, 3.5)),
]

for txt, xy, xytext in annotations:
    ax.annotate(txt, xy=xy, xytext=xytext,
                arrowprops=arrow_kw, **txt_kw)

ax.set_title('Аннотований лістинг команди top', fontsize=13,
             fontweight='bold', color='white', pad=8)
plt.tight_layout()
plt.savefig(f'{BASE}/fig1_annotated.png', bbox_inches='tight',
            facecolor='#0F172A')
plt.close()
print("fig1 OK")

# ── Рис 2: CPU pie + Memory bar ──────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# CPU pie
cpu_vals   = [52.3, 17.7, 19.8, 10.2]
cpu_labels = ['User (us)\n52.3%', 'System (sy)\n17.7%',
              'I/O Wait (wa)\n19.8%', 'Idle (id)\n10.2%']
cpu_colors = [BLUE, PURPLE, RED, GREEN]
explode    = (0, 0, 0.08, 0)
wedges, _, autotexts = ax1.pie(
    cpu_vals, labels=cpu_labels, colors=cpu_colors, explode=explode,
    autopct='%1.1f%%', startangle=90, pctdistance=0.6,
    wedgeprops=dict(edgecolor='white', linewidth=1.5))
for at in autotexts: at.set_fontsize(8)
ax1.set_title('Розподіл часу CPU', fontsize=12, fontweight='bold')
# Виноска для wa
ax1.annotate('КРИТИЧНО:\nвисокий I/O Wait',
             xy=(-0.55, -0.6), xytext=(-1.3, -1.0),
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
             fontsize=9, color=RED, fontweight='bold')

# Memory stacked bar
categories = ['RAM (4.0 ГБ)', 'Swap (4.0 ГБ)']
used   = [3971588/1024, 1984/1024]
free   = [175680/1024,  4094548/1024]
cached = [236316/1024,  1634360/1024]

x = np.arange(2)
w = 0.45
b1 = ax2.bar(x, used,   w, label='Використано', color=RED,    alpha=0.85)
b2 = ax2.bar(x, cached, w, bottom=used, label='Буфери/Кеш', color=ORANGE, alpha=0.7)
b3 = ax2.bar(x, free,   w, bottom=[u+c for u,c in zip(used,cached)],
             label='Вільно', color=GREEN, alpha=0.7)

ax2.set_xticks(x); ax2.set_xticklabels(categories, fontsize=10)
ax2.set_ylabel('МБ', fontsize=10)
ax2.set_title('Використання пам\'яті', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v,_: f'{v/1024:.1f} ГБ'))

# % підписи
for i, (u, tot) in enumerate(zip(used, [4147268/1024, 4096532/1024])):
    pct = u / tot * 100
    ax2.text(i, u/2, f'{pct:.1f}%', ha='center', va='center',
             fontsize=10, fontweight='bold', color='white')

ax2.axhline(4147268/1024 * 0.9, color=RED, linestyle='--', linewidth=1,
            label='90% поріг RAM', alpha=0.6)
ax2.text(1.35, 4147268/1024 * 0.91, '90% поріг', fontsize=8, color=RED)

plt.tight_layout()
plt.savefig(f'{BASE}/fig2_cpu_mem.png', bbox_inches='tight')
plt.close()
print("fig2 OK")

# ── Рис 3: Top-процеси по CPU ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5.5))

procs = [
    ('mysqld',       34.5, ORANGE, 'S'),
    ('php Z(29790)',  15.9, RED,    'Z'),
    ('php Z(29791)',  15.9, RED,    'Z'),
    ('php Z(29787)',  13.6, RED,    'Z'),
    ('php Z(29784)',   9.6, RED,    'Z'),
    ('php R(29807)',   7.6, BLUE,   'R'),
    ('php S(29804)',   4.6, '#60A5FA', 'S'),
    ('psmon(21958)',   3.3, PURPLE, 'S'),
    ('php Z(29808)',   3.0, RED,    'Z'),
    ('psmon(17989)',   1.7, PURPLE, 'S'),
]
names  = [p[0] for p in procs]
vals   = [p[1] for p in procs]
bcolors= [p[2] for p in procs]
states = [p[3] for p in procs]

bars = ax.barh(range(len(names)), vals, color=bcolors, alpha=0.85,
               edgecolor='white', linewidth=0.5)
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('%CPU', fontsize=11)
ax.set_title('Топ-10 процесів за навантаженням на CPU', fontsize=12, fontweight='bold')
ax.axvline(x=100, color=GRAY, linestyle='--', linewidth=1, alpha=0.5)
ax.text(100.5, -0.5, '100% (1 ядро)', fontsize=8, color=GRAY)

for i, (bar, v, s) in enumerate(zip(bars, vals, states)):
    ax.text(v + 0.3, i, f'{v}%  [{s}]', va='center', fontsize=8.5,
            fontweight='bold' if s == 'Z' else 'normal',
            color=RED if s == 'Z' else DARK)

legend_patches = [
    mpatches.Patch(color=ORANGE, label='mysqld (S – sleeping)'),
    mpatches.Patch(color=RED,    label='php <defunct> (Z – zombie)'),
    mpatches.Patch(color=BLUE,   label='php (R – running)'),
    mpatches.Patch(color=PURPLE, label='psmon (S – sleeping)'),
]
ax.legend(handles=legend_patches, fontsize=8.5, loc='lower right')
plt.tight_layout()
plt.savefig(f'{BASE}/fig3_top_procs.png', bbox_inches='tight')
plt.close()
print("fig3 OK")

# ── Рис 4: Кількість CPU — обґрунтування ─────────────────────
fig, ax = plt.subplots(figsize=(11, 4))
ax.axis('off')

data = [
    ['Аргумент', 'Факт', 'Висновок'],
    ['Сума рядка CPU(s)',
     '52.3+17.7+19.8+10.2 = 100.0%',
     'top нормує на 100% × N_CPU\nСума = 100 → N_CPU = 1'],
    ['Load average (1 хв)',
     '1.10',
     'LA ≈ 1.0 при повністю\nзавантаженому 1 ядрі'],
    ['Idle = 10.2%',
     '~90% CPU зайнято',
     'Узгоджується з LA ≈ 1.1\nна 1 ядрі'],
    ['mysqld %CPU = 34.5%',
     'Один процес ≠ >100%',
     'На 2+ ядрах один потік\nне міг би показати >100%'],
    ['Zombie %CPU сума',
     '~58% (артефакт зйомки)',
     'Частина йде до загального\nпулу, не додаткове ядро'],
]

t = Table(data, colWidths=[5*cm, 5.5*cm, 6.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), colors.HexColor(DARK)),
    ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
    ('FONTNAME',    (0,0), (-1,0), 'RB'),
    ('FONTNAME',    (0,1), (-1,-1),'R'),
    ('FONTSIZE',    (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#EFF6FF')]),
    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('TOPPADDING',  (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND',  (0,1), (-1,1), colors.HexColor('#FEF3C7')),
    ('FONTNAME',    (0,1), (-1,1), 'RB'),
]))
ax.set_title('Обґрунтування кількості CPU (1 логічне ядро)', fontsize=12,
             fontweight='bold', pad=10)
fig.subplots_adjust(top=0.88)

ax.axis('off')
col_labels = data[0]
cell_data  = data[1:]
mpl_table = ax.table(cellText=cell_data, colLabels=col_labels,
                      cellLoc='left', loc='center',
                      colWidths=[0.28, 0.33, 0.39])
mpl_table.auto_set_font_size(False)
mpl_table.set_fontsize(9)
mpl_table.scale(1, 2.0)
for (r,c), cell in mpl_table.get_celld().items():
    cell.set_edgecolor('#CBD5E1')
    if r == 0:
        cell.set_facecolor(DARK); cell.set_text_props(color='white', fontweight='bold')
    elif r % 2 == 0:
        cell.set_facecolor('#EFF6FF')
    if r == 1:
        cell.set_facecolor('#FEF3C7')

plt.tight_layout()
plt.savefig(f'{BASE}/fig4_cpu_count.png', bbox_inches='tight')
plt.close()
print("fig4 OK")

# ════════════════════════════════════════════════════════════════
# PDF ЗВІТ
# ════════════════════════════════════════════════════════════════
from PIL import Image as PILImage

def img_elem(fname, w=16):
    path = f'{BASE}/{fname}'
    with PILImage.open(path) as im:
        iw, ih = im.size
    return Image(path, width=w*cm, height=w*cm*ih/iw)

W, H = A4
doc = SimpleDocTemplate(f'{BASE}/top_analysis_report.pdf', pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)

C_ACCENT = colors.HexColor(BLUE)
C_DARK   = colors.HexColor(DARK)
C_RED    = colors.HexColor(RED)
C_ORANGE = colors.HexColor(ORANGE)
C_GREEN  = colors.HexColor(GREEN)
C_GRAY   = colors.HexColor('#64748B')
C_LIGHT  = colors.HexColor(LIGHT)

def sty(name, **kw):
    presets = {
        'title':   dict(fontName='RB', fontSize=20, textColor=C_DARK, spaceAfter=4, alignment=TA_CENTER),
        'sub':     dict(fontName='R',  fontSize=11, textColor=C_GRAY, spaceAfter=3, alignment=TA_CENTER),
        'h1':      dict(fontName='RB', fontSize=14, textColor=C_DARK, spaceBefore=12, spaceAfter=5),
        'h2':      dict(fontName='RB', fontSize=11, textColor=C_ACCENT, spaceBefore=8, spaceAfter=4),
        'body':    dict(fontName='R',  fontSize=10, textColor=colors.black, spaceAfter=4, leading=15, alignment=TA_JUSTIFY),
        'warn':    dict(fontName='RB', fontSize=10, textColor=C_RED,
                        backColor=colors.HexColor('#FEF2F2'),
                        borderPadding=8, spaceAfter=5, leading=15, alignment=TA_JUSTIFY),
        'ok':      dict(fontName='R',  fontSize=10, textColor=colors.HexColor('#065F46'),
                        backColor=colors.HexColor('#ECFDF5'),
                        borderPadding=8, spaceAfter=5, leading=15),
        'concl':   dict(fontName='RB', fontSize=11, textColor=C_DARK,
                        backColor=colors.HexColor('#EFF6FF'),
                        borderPadding=10, spaceAfter=6, leading=17, alignment=TA_JUSTIFY),
        'caption': dict(fontName='R',  fontSize=8.5, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=8),
        'mono':    dict(fontName='R',  fontSize=8.5, textColor=colors.HexColor('#1E293B'),
                        backColor=colors.HexColor('#F1F5F9'), borderPadding=6, spaceAfter=4, leading=13),
    }
    d = presets[name]; d.update(kw); return ParagraphStyle(name + str(id(kw)), **d)

def p(text, style='body'):  return Paragraph(text, sty(style))
def sp(h=0.3):              return Spacer(1, h*cm)
def hr():                   return HRFlowable(width='100%', thickness=1, color=C_LIGHT, spaceAfter=6)

def tbl(data, widths, header_dark=True, alt_color='#EFF6FF'):
    t = Table(data, colWidths=[w*cm for w in widths])
    style = [
        ('FONTNAME',    (0,1),(-1,-1),'R'),
        ('FONTSIZE',    (0,0),(-1,-1), 9),
        ('GRID',        (0,0),(-1,-1), 0.4, colors.HexColor('#CBD5E1')),
        ('TOPPADDING',  (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',      (0,0),(-1,-1),'MIDDLE'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor(alt_color)]),
    ]
    if header_dark:
        style += [
            ('BACKGROUND', (0,0),(-1,0), C_DARK),
            ('TEXTCOLOR',  (0,0),(-1,0), colors.white),
            ('FONTNAME',   (0,0),(-1,0), 'RB'),
        ]
    t.setStyle(TableStyle(style))
    return t

story = []

# ── Титул ────────────────────────────────────────────────────
story += [
    sp(2.5),
    p('Аналіз навантаження на систему', 'title'),
    p('за виводом команди <b>top</b>', 'title'),
    sp(0.3), hr(), sp(0.2),
    p('Лабораторна робота з курсу «Операційні системи»', 'sub'),
    p('Час знімку: 17:25:19  |  Аптайм: 104 дні 13:31  |  Сервер під навантаженням', 'sub'),
    sp(0.5),
]

# Зведена таблиця на титульній
summary = [
    ['Показник', 'Значення', 'Оцінка'],
    ['Активних процесів (running)', '5',          'Норма'],
    ['Zombie-процесів',             '6',          'ПРОБЛЕМА'],
    ['CPU Idle',                    '10.2%',      'Критично мало'],
    ['CPU I/O Wait',                '19.8%',      'Критично'],
    ['RAM зайнято',                 '95.7%',      'Критично'],
    ['Swap зайнято',                '0.05%',      'OK'],
    ['Load average (1/5/15 хв)',    '1.10 / 1.25 / 0.82', 'Помірне'],
    ['Кількість CPU (ОС)',          '1 логічне ядро', 'Встановлено'],
]
t = Table(summary, colWidths=[6.5*cm, 5*cm, 4.5*cm])
ts_title = TableStyle([
    ('BACKGROUND',   (0,0),(-1,0), C_DARK),
    ('TEXTCOLOR',    (0,0),(-1,0), colors.white),
    ('FONTNAME',     (0,0),(-1,0), 'RB'),
    ('FONTNAME',     (0,1),(-1,-1),'R'),
    ('FONTSIZE',     (0,0),(-1,-1), 9.5),
    ('GRID',         (0,0),(-1,-1), 0.4, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('LEFTPADDING',  (0,0),(-1,-1), 9),
    # Виділення проблемних рядків
    ('BACKGROUND',   (0,2),(-1,2), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,2),(2,2),   C_RED),
    ('FONTNAME',     (2,2),(2,2),   'RB'),
    ('BACKGROUND',   (0,3),(-1,3), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,3),(2,3),   C_RED),
    ('FONTNAME',     (2,3),(2,3),   'RB'),
    ('BACKGROUND',   (0,4),(-1,4), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,4),(2,4),   C_RED),
    ('FONTNAME',     (2,4),(2,4),   'RB'),
    ('BACKGROUND',   (0,5),(-1,5), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,5),(2,5),   C_RED),
    ('FONTNAME',     (2,5),(2,5),   'RB'),
    ('BACKGROUND',   (0,6),(-1,6), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,6),(2,6),   C_RED),
    ('FONTNAME',     (2,6),(2,6),   'RB'),
    ('BACKGROUND',   (0,7),(-1,7), colors.HexColor('#ECFDF5')),
    ('TEXTCOLOR',    (2,7),(2,7),   C_GREEN),
])
t.setStyle(ts_title)
story += [t, PageBreak()]

# ── Розділ 1: Аннотований лістинг ────────────────────────────
story += [
    p('1. Аннотований лістинг команди top', 'h1'), hr(),
    p('Нижче наведено вивід команди top з підписаними елементами. '
      'Жовтим виділено проблемні зони, червоним фоном — zombie-процеси '
      'та MySQL.', 'body'),
    sp(0.2),
    img_elem('fig1_annotated.png', w=17),
    p('Рис. 1 — Аннотований вивід top. Стрілки вказують на ключові '
      'елементи заголовку та процеси з аномальними показниками.', 'caption'),
    sp(0.3),
]

# Таблиця-розшифровка полів
fields = [
    ['Поле / Рядок', 'Значення', 'Пояснення'],
    ['top - 17:25:19', 'Поточний час', 'Момент знімку'],
    ['up 104 days, 13:31', 'Аптайм системи', 'Сервер не перезавантажувався 104 дні'],
    ['4 users', 'Кількість сесій', 'Активні термінальні сесії'],
    ['load average: 1.10, 1.25, 0.82', 'LA за 1/5/15 хв', 'Середня довжина черги процесів на CPU'],
    ['Tasks: 254 total', 'Всього процесів', 'Включно зі сплячими'],
    ['5 running', 'Активно виконуються', 'Займають CPU прямо зараз'],
    ['243 sleeping', 'Очікують події', 'I/O, таймер, сигнал — норма'],
    ['6 zombie', 'Завершились, не "підібрані"', 'Батьківський процес не викликав wait()'],
    ['%us = 52.3%', 'User-space CPU', 'Застосунки (mysql, php, httpd)'],
    ['%sy = 17.7%', 'Kernel-space CPU', 'Системні виклики ядра'],
    ['%wa = 19.8%', 'I/O Wait', 'CPU чекає на диск — ВУЗЬКЕ МІСЦЕ'],
    ['%id = 10.2%', 'Idle (вільний CPU)', 'Майже не залишається вільного часу'],
    ['Mem: 95.7% used', 'Оперативна пам\'ять', '3.79 ГБ з 3.95 ГБ зайнято'],
    ['Swap: 0.05% used', 'Своп практично вільний', 'Активного свопінгу немає'],
]

fields_tbl = tbl(fields, [3.8, 4.0, 8.2])
# Виділити wa рядок
fields_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,12),(-1,12), colors.HexColor('#FEF2F2')),
    ('FONTNAME',   (0,12),(-1,12), 'RB'),
]))
story += [fields_tbl, sp(0.3)]

# Заголовки колонок процесів
proc_cols = [
    ['Колонка', 'Зміст'],
    ['PID',     'Ідентифікатор процесу'],
    ['USER',    'Власник процесу'],
    ['PR',      'Пріоритет планувальника ОС'],
    ['NI',      'Nice-значення (корекція пріоритету користувачем)'],
    ['VIRT',    'Загальний виртуальний адресний простір'],
    ['RES',     'Реальна фізична пам\'ять (Resident Set Size)'],
    ['SHR',     'Розділювана пам\'ять (shared libs тощо)'],
    ['S',       'Стан: R=running, S=sleeping, Z=zombie, D=uninterruptible sleep'],
    ['%CPU',    'Частка часу CPU за останній інтервал'],
    ['%MEM',    'Частка фізичної RAM'],
    ['TIME+',   'Загальний процесорний час з моменту запуску'],
    ['COMMAND', 'Назва програми'],
]
story += [
    p('Розшифровка колонок таблиці процесів:', 'h2'),
    tbl(proc_cols, [2.5, 13.5]),
    PageBreak(),
]

# ── Розділ 2: Характеристика системи ─────────────────────────
story += [
    p('2. Характеристика ситуації в системі', 'h1'), hr(),
    img_elem('fig2_cpu_mem.png', w=15.5),
    p('Рис. 2 — Розподіл часу CPU (ліворуч) та використання пам\'яті (праворуч).', 'caption'),
    sp(0.2),
]

story += [
    p('2.1  Завантаження CPU', 'h2'),
    p('Система завантажена на <b>~90% CPU</b> (idle лише 10.2%). '
      'Найтривожніший показник — <b>I/O Wait 19.8%</b>: майже п\'ята частина '
      'всього процесорного часу витрачається на очікування диску. '
      'Це означає, що CPU простоює через повільні дискові операції, '
      'і саме дисковий I/O є <b>основним вузьким місцем</b> системи.',
      'warn'),

    p('2.2  Стан процесів', 'h2'),
    p('В системі присутні <b>6 zombie-процесів</b> — усі є дочірніми процесами PHP. '
      'Зомбі-процес — це процес, який завершив виконання, але запис про нього '
      'залишається у таблиці процесів, бо батьківський процес ще не зчитав '
      'його код завершення (не викликав <i>wait()</i>). Самі по собі зомбі '
      'не споживають CPU чи RAM, проте займають PID і свідчать про помилку '
      'у коді або конфігурації батьківського процесу (PHP-FPM / FastCGI).',
      'warn'),

    p('2.3  Пам\'ять', 'h2'),
    p('RAM зайнята на <b>95.7%</b> (3.79 ГБ з 3.95 ГБ). '
      'З них ~236 МБ — буфери ядра, ~1.6 ГБ — дисковий кеш. '
      'Якщо відняти кеш, "реально вільної" пам\'яті залишається ~1.8 ГБ, '
      'але вона не є резервом для нових процесів у звичайному розумінні. '
      'Позитивний момент: <b>Swap зайнятий лише на 0.05%</b> — активного '
      'свопінгу немає, тому деградація через підкачку не спостерігається.',
      'body'),

    p('2.4  Ключові процеси', 'h2'),
]

story += [img_elem('fig3_top_procs.png', w=15.5),
          p('Рис. 3 — Топ-10 процесів за навантаженням CPU.', 'caption')]

proc_analysis = [
    ['Процес', 'CPU', 'Стан', 'Аналіз'],
    ['mysqld (PID 1722)',    '34.5%', 'S', 'Основний споживач CPU. 260+ годин сумарного CPU-часу. '
                                           'Активні запити до БД або неоптимізовані запити'],
    ['php <defunct> ×5',    '~58%',  'Z', 'Zombie-процеси PHP. CPU% — артефакт останнього '
                                           'інтервалу перед загибеллю. Реально CPU не займають'],
    ['php R (PID 29807)',    '7.6%',  'R', 'Активний PHP-воркер, виконує запит прямо зараз'],
    ['psmon (PID 21958)',    '3.3%',  'S', '667 годин CPU за увесь час роботи — підозріло '
                                           'висока сумарна витрата для моніторингового процесу'],
    ['psmon (PID 17989)',    '1.7%',  'S', '689 годин CPU. Два екземпляри psmon разом '
                                           'назбирали ~1356 годин CPU-часу'],
    ['httpd ×15+',          '~7%',   'S', 'Apache workers — кожен займає ~38 МБ RAM. '
                                           '15+ воркерів = ~570 МБ тільки на httpd'],
]
story += [sp(0.2), tbl(proc_analysis, [3.5, 1.5, 1.5, 9.5]), PageBreak()]

# ── Розділ 3: Кількість CPU ───────────────────────────────────
story += [
    p('3. Кількість процесорів з точки зору ОС', 'h1'), hr(),
    p('<b>Висновок: система має 1 логічний процесор (ядро).</b>', 'concl'),
    sp(0.3),
    img_elem('fig4_cpu_count.png', w=16),
    p('Рис. 4 — Аргументи на користь 1 логічного CPU.', 'caption'),
    sp(0.2),
    p('Головний аргумент — математичний: рядок <b>Cpu(s)</b> у top при '
      'режимі за замовчуванням (без натискання «1») показує <i>усереднені</i> '
      'значення по всіх ядрах, нормовані так, що сума завжди дорівнює 100%. '
      '52.3 + 17.7 + 0.0 + 10.2 + 19.8 + 0.0 + 0.0 = <b>100.0%</b> — '
      'точна рівність підтверджує, що нормування відбулося на 1 ядро.', 'body'),
    p('Load average 1.10 означає, що в середньому 1.1 процесу одночасно '
      'претендують на CPU. Для однопроцесорної системи це відповідає '
      'завантаженню ~110% (черга не порожня), що узгоджується з idle=10.2%.',
      'body'),
    PageBreak(),
]

# ── Розділ 4: Поради ─────────────────────────────────────────
story += [
    p('4. Проблемні місця та рекомендації', 'h1'), hr(),
]

problems = [
    ['#', 'Проблема', 'Серйозність', 'Рекомендація'],
    ['1', 'I/O Wait 19.8%\n(дисковий bottleneck)',
          'КРИТИЧНО',
          'Увімкнути slow query log у MySQL (long_query_time=1). '
          'Перевірити iostat/iotop — визначити який процес генерує I/O. '
          'Розглянути перехід на SSD або додавання RAM для збільшення '
          'дискового кешу ядра.'],
    ['2', '6 zombie PHP-процесів',
          'ВАЖЛИВО',
          'Перезапустити PHP-FPM: service php-fpm restart. '
          'Перевірити логи PHP-FPM на предмет зависань воркерів. '
          'Налаштувати pm.max_requests та request_terminate_timeout.'],
    ['3', 'MySQL споживає 34.5% CPU\n(260+ год накопиченого часу)',
          'ВАЖЛИВО',
          'Увімкнути slow query log, запустити mysqldumpslow. '
          'Перевірити innodb_buffer_pool_size (рекомендується 50-70% RAM = ~2 ГБ). '
          'Додати індекси до "гарячих" таблиць. '
          'Розглянути query cache або кешування на рівні застосунку.'],
    ['4', 'RAM 95.7% зайнято\n(175 МБ вільно)',
          'ВАЖЛИВО',
          'Збільшити обсяг RAM до 8+ ГБ — це знизить і I/O Wait '
          '(більший дисковий кеш), і ризик OOM Killer. '
          'Або зменшити кількість Apache-воркерів (MaxClients): '
          '15×38 МБ = 570 МБ лише на httpd.'],
    ['5', 'psmon: ~1356 год\nсукупного CPU (2 процеси)',
          'УВАГА',
          'З\'ясувати що робить psmon — нетиповий показник для '
          'моніторингового демона. Перевірити логи, можливо процес '
          'застряг у циклі або виконує надмірне сканування.'],
    ['6', 'Apache prefork: багато воркерів\nз великим RSS (~38 МБ кожен)',
          'ПОРАДА',
          'Розглянути міграцію на Nginx + PHP-FPM або Apache з '
          'mpm_event. Event-based архітектура обслуговує більше '
          'з\'єднань при меншому споживанні пам\'яті.'],
    ['7', 'httpd PID 8011 у стані D\n(uninterruptible sleep)',
          'УВАГА',
          'Стан D означає очікування I/O, з якого процес не можна '
          'перервати. Пов\'язано з проблемою #1 (дисковий I/O). '
          'При усуненні bottleneck зникне само.'],
]

pt = Table(problems, colWidths=[0.7*cm, 4.2*cm, 2.5*cm, 8.6*cm])
pts = TableStyle([
    ('BACKGROUND',   (0,0),(-1,0), C_DARK),
    ('TEXTCOLOR',    (0,0),(-1,0), colors.white),
    ('FONTNAME',     (0,0),(-1,0), 'RB'),
    ('FONTNAME',     (0,1),(-1,-1),'R'),
    ('FONTSIZE',     (0,0),(-1,-1), 8.5),
    ('GRID',         (0,0),(-1,-1), 0.4, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('LEFTPADDING',  (0,0),(-1,-1), 7),
    ('VALIGN',       (0,0),(-1,-1), 'TOP'),
    # Критичні
    ('BACKGROUND',   (2,1),(2,1), colors.HexColor('#FEF2F2')),
    ('TEXTCOLOR',    (2,1),(2,1), C_RED),
    ('FONTNAME',     (2,1),(2,1), 'RB'),
    ('BACKGROUND',   (2,2),(2,2), colors.HexColor('#FEF9C3')),
    ('TEXTCOLOR',    (2,2),(2,2), colors.HexColor('#92400E')),
    ('FONTNAME',     (2,2),(2,2), 'RB'),
    ('BACKGROUND',   (2,3),(2,3), colors.HexColor('#FEF9C3')),
    ('TEXTCOLOR',    (2,3),(2,3), colors.HexColor('#92400E')),
    ('FONTNAME',     (2,3),(2,3), 'RB'),
    ('BACKGROUND',   (2,4),(2,4), colors.HexColor('#FEF9C3')),
    ('TEXTCOLOR',    (2,4),(2,4), colors.HexColor('#92400E')),
    ('FONTNAME',     (2,4),(2,4), 'RB'),
])
pt.setStyle(pts)
story += [pt, sp(0.5)]

story += [
    p('Пріоритетний план дій:', 'h2'),
    p('1. <b>Негайно</b> — перезапустити PHP-FPM для усунення zombie-процесів.', 'body'),
    p('2. <b>Сьогодні</b> — увімкнути slow query log у MySQL, запустити '
      '<i>mysqldumpslow</i> і <i>iotop</i> для точної локалізації I/O-навантаження.', 'body'),
    p('3. <b>Найближчим часом</b> — збільшити innodb_buffer_pool_size до ~2 ГБ, '
      'оптимізувати запити за результатами slow log.', 'body'),
    p('4. <b>Планово</b> — розглянути збільшення RAM до 8 ГБ та/або '
      'перехід із Apache prefork на Nginx + PHP-FPM.', 'body'),
    sp(0.4), hr(),
    p('<i>Аналіз виконано на основі одного знімку top (17:25:19). '
      'Для повноцінної діагностики рекомендується моніторинг у динаміці '
      '(vmstat, iostat, sar) та аналіз логів MySQL і PHP-FPM.</i>', 'caption'),
]

doc.build(story)
print(f"PDF: {BASE}/top_analysis_report.pdf")
