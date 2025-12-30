# -*- coding: utf-8 -*-
"""语文阅读故事内容"""

import random
from datetime import date

# 故事列表 - 适合一年级小朋友的经典故事
STORIES = [
    {
        "id": 1,
        "title": "小蝌蚪找妈妈",
        "image": "🐸",
        "content": """
<p>
<ruby>春<rt>chūn</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>了<rt>le</rt></ruby>，<ruby>池<rt>chí</rt></ruby><ruby>塘<rt>táng</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>和<rt>huo</rt></ruby><ruby>了<rt>le</rt></ruby>。<ruby>青<rt>qīng</rt></ruby><ruby>蛙<rt>wā</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>草<rt>cǎo</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>生<rt>shēng</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>很<rt>hěn</rt></ruby><ruby>多<rt>duō</rt></ruby><ruby>黑<rt>hēi</rt></ruby><ruby>黑<rt>hēi</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>圆<rt>yuán</rt></ruby><ruby>圆<rt>yuán</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>卵<rt>luǎn</rt></ruby>。
</p>
<p>
<ruby>过<rt>guò</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>几<rt>jǐ</rt></ruby><ruby>天<rt>tiān</rt></ruby>，<ruby>卵<rt>luǎn</rt></ruby><ruby>变<rt>biàn</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>群<rt>qún</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby>。<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>脑<rt>nǎo</rt></ruby><ruby>袋<rt>dài</rt></ruby>，<ruby>黑<rt>hēi</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>身<rt>shēn</rt></ruby><ruby>子<rt>zi</rt></ruby>，<ruby>甩<rt>shuǎi</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>长<rt>cháng</rt></ruby><ruby>长<rt>cháng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby>，<ruby>快<rt>kuài</rt></ruby><ruby>活<rt>huó</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>去<rt>qù</rt></ruby>。
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>啊<rt>a</rt></ruby><ruby>游<rt>yóu</rt></ruby>，<ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby><ruby>鲤<rt>lǐ</rt></ruby><ruby>鱼<rt>yú</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>教<rt>jiāo</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>鲤<rt>lǐ</rt></ruby><ruby>鱼<rt>yú</rt></ruby><ruby>捉<rt>zhuō</rt></ruby><ruby>食<rt>shí</rt></ruby><ruby>吃<rt>chī</rt></ruby>。<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>想<rt>xiǎng</rt></ruby>：<ruby>我<rt>wǒ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>哪<rt>nǎ</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>呢<rt>ne</rt></ruby>？
</p>
<p>
<ruby>他<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>问<rt>wèn</rt></ruby><ruby>鲤<rt>lǐ</rt></ruby><ruby>鱼<rt>yú</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>："<ruby>您<rt>nín</rt></ruby><ruby>好<rt>hǎo</rt></ruby>！<ruby>请<rt>qǐng</rt></ruby><ruby>问<rt>wèn</rt></ruby><ruby>我<rt>wǒ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>哪<rt>nǎ</rt></ruby><ruby>里<rt>lǐ</rt></ruby>？"
</p>
<p>
<ruby>鲤<rt>lǐ</rt></ruby><ruby>鱼<rt>yú</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>说<rt>shuō</rt></ruby>："<ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>眼<rt>yǎn</rt></ruby><ruby>睛<rt>jīng</rt></ruby>，<ruby>嘴<rt>zuǐ</rt></ruby><ruby>巴<rt>ba</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>阔<rt>kuò</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>大<rt>dà</rt></ruby>。<ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>那<rt>nà</rt></ruby><ruby>边<rt>biān</rt></ruby><ruby>去<rt>qù</rt></ruby><ruby>找<rt>zhǎo</rt></ruby><ruby>吧<rt>ba</rt></ruby>！"
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>啊<rt>a</rt></ruby><ruby>游<rt>yóu</rt></ruby>，<ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>游<rt>yóu</rt></ruby>。<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>眼<rt>yǎn</rt></ruby><ruby>睛<rt>jīng</rt></ruby>，<ruby>嘴<rt>zuǐ</rt></ruby><ruby>巴<rt>ba</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>阔<rt>kuò</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>大<rt>dà</rt></ruby>。
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>兴<rt>xìng</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>叫<rt>jiào</rt></ruby>："<ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>！<ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>！"
</p>
<p>
<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>说<rt>shuō</rt></ruby>："<ruby>我<rt>wǒ</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>。<ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>穿<rt>chuān</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>衣<rt>yī</rt></ruby><ruby>裳<rt>shang</rt></ruby>，<ruby>唱<rt>chàng</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>歌<rt>gē</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>呱<rt>guā</rt></ruby><ruby>呱<rt>guā</rt></ruby><ruby>叫<rt>jiào</rt></ruby>。<ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>那<rt>nà</rt></ruby><ruby>边<rt>biān</rt></ruby><ruby>去<rt>qù</rt></ruby><ruby>找<rt>zhǎo</rt></ruby><ruby>吧<rt>ba</rt></ruby>！"
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>啊<rt>a</rt></ruby><ruby>游<rt>yóu</rt></ruby>，<ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>青<rt>qīng</rt></ruby><ruby>蛙<rt>wā</rt></ruby><ruby>坐<rt>zuò</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby><ruby>上<rt>shàng</rt></ruby>。<ruby>青<rt>qīng</rt></ruby><ruby>蛙<rt>wā</rt></ruby><ruby>穿<rt>chuān</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>衣<rt>yī</rt></ruby><ruby>裳<rt>shang</rt></ruby>，<ruby>露<rt>lù</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>雪<rt>xuě</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>肚<rt>dù</rt></ruby><ruby>皮<rt>pí</rt></ruby>，<ruby>鼓<rt>gǔ</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>对<rt>duì</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>眼<rt>yǎn</rt></ruby><ruby>睛<rt>jīng</rt></ruby>。
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>兴<rt>xìng</rt></ruby><ruby>极<rt>jí</rt></ruby><ruby>了<rt>le</rt></ruby>，<ruby>游<rt>yóu</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>去<rt>qù</rt></ruby><ruby>叫<rt>jiào</rt></ruby>："<ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>！<ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>！"
</p>
<p>
<ruby>青<rt>qīng</rt></ruby><ruby>蛙<rt>wā</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby><ruby>低<rt>dī</rt></ruby><ruby>头<rt>tóu</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>看<rt>kàn</rt></ruby>，<ruby>笑<rt>xiào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>说<rt>shuō</rt></ruby>："<ruby>好<rt>hǎo</rt></ruby><ruby>孩<rt>hái</rt></ruby><ruby>子<rt>zi</rt></ruby>，<ruby>你<rt>nǐ</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>已<rt>yǐ</rt></ruby><ruby>经<rt>jīng</rt></ruby><ruby>长<rt>zhǎng</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>了<rt>le</rt></ruby>！<ruby>快<rt>kuài</rt></ruby><ruby>跳<rt>tiào</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>吧<rt>ba</rt></ruby>！"
</p>
<p>
<ruby>小<rt>xiǎo</rt></ruby><ruby>蝌<rt>kē</rt></ruby><ruby>蚪<rt>dǒu</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>后<rt>hòu</rt></ruby><ruby>腿<rt>tuǐ</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>蹬<rt>dēng</rt></ruby>，<ruby>跳<rt>tiào</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby>。<ruby>他<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>跟<rt>gēn</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby>，<ruby>天<rt>tiān</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>去<rt>qù</rt></ruby><ruby>捉<rt>zhuō</rt></ruby><ruby>害<rt>hài</rt></ruby><ruby>虫<rt>chóng</rt></ruby>。
</p>
"""
    },
    {
        "id": 2,
        "title": "乌鸦喝水",
        "image": "🐦",
        "content": """
<p>
<ruby>一<rt>yī</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>口<rt>kǒu</rt></ruby><ruby>渴<rt>kě</rt></ruby><ruby>了<rt>le</rt></ruby>，<ruby>到<rt>dào</rt></ruby><ruby>处<rt>chù</rt></ruby><ruby>找<rt>zhǎo</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>喝<rt>hē</rt></ruby>。<ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>瓶<rt>píng</rt></ruby><ruby>子<rt>zi</rt></ruby>，<ruby>瓶<rt>píng</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>水<rt>shuǐ</rt></ruby>。<ruby>可<rt>kě</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>瓶<rt>píng</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>不<rt>bù</rt></ruby><ruby>多<rt>duō</rt></ruby>，<ruby>瓶<rt>píng</rt></ruby><ruby>口<rt>kǒu</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>小<rt>xiǎo</rt></ruby>，<ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>喝<rt>hē</rt></ruby><ruby>不<rt>bù</rt></ruby><ruby>着<rt>zháo</rt></ruby><ruby>水<rt>shuǐ</rt></ruby>。<ruby>怎<rt>zěn</rt></ruby><ruby>么<rt>me</rt></ruby><ruby>办<rt>bàn</rt></ruby><ruby>呢<rt>ne</rt></ruby>？
</p>
<p>
<ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby><ruby>旁<rt>páng</rt></ruby><ruby>边<rt>biān</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>许<rt>xǔ</rt></ruby><ruby>多<rt>duō</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>石<rt>shí</rt></ruby><ruby>子<rt>zi</rt></ruby>。<ruby>它<rt>tā</rt></ruby><ruby>想<rt>xiǎng</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>办<rt>bàn</rt></ruby><ruby>法<rt>fǎ</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>了<rt>le</rt></ruby>。
</p>
<p>
<ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>把<rt>bǎ</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>石<rt>shí</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>颗<rt>kē</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>颗<rt>kē</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>放<rt>fàng</rt></ruby><ruby>进<rt>jìn</rt></ruby><ruby>瓶<rt>píng</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>里<rt>lǐ</rt></ruby>。<ruby>瓶<rt>píng</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>渐<rt>jiàn</rt></ruby><ruby>渐<rt>jiàn</rt></ruby><ruby>升<rt>shēng</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>了<rt>le</rt></ruby>，<ruby>乌<rt>wū</rt></ruby><ruby>鸦<rt>yā</rt></ruby><ruby>就<rt>jiù</rt></ruby><ruby>喝<rt>hē</rt></ruby><ruby>着<rt>zháo</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>了<rt>le</rt></ruby>。
</p>
<p>
<ruby>这<rt>zhè</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>故<rt>gù</rt></ruby><ruby>事<rt>shì</rt></ruby><ruby>告<rt>gào</rt></ruby><ruby>诉<rt>sù</rt></ruby><ruby>我<rt>wǒ</rt></ruby><ruby>们<rt>men</rt></ruby>：<ruby>遇<rt>yù</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>困<rt>kùn</rt></ruby><ruby>难<rt>nán</rt></ruby><ruby>要<rt>yào</rt></ruby><ruby>动<rt>dòng</rt></ruby><ruby>脑<rt>nǎo</rt></ruby><ruby>筋<rt>jīn</rt></ruby><ruby>想<rt>xiǎng</rt></ruby><ruby>办<rt>bàn</rt></ruby><ruby>法<rt>fǎ</rt></ruby>。
</p>
"""
    },
    {
        "id": 3,
        "title": "龟兔赛跑",
        "image": "🐢🐰",
        "content": """
<p>
<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>跑<rt>pǎo</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>快<rt>kuài</rt></ruby>，<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>爬<rt>pá</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>慢<rt>màn</rt></ruby>。<ruby>有<rt>yǒu</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>天<rt>tiān</rt></ruby>，<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>要<rt>yào</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>赛<rt>sài</rt></ruby><ruby>跑<rt>pǎo</rt></ruby>。<ruby>许<rt>xǔ</rt></ruby><ruby>多<rt>duō</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>动<rt>dòng</rt></ruby><ruby>物<rt>wù</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>看<rt>kàn</rt></ruby><ruby>热<rt>rè</rt></ruby><ruby>闹<rt>nao</rt></ruby>。
</p>
<p>
<ruby>比<rt>bǐ</rt></ruby><ruby>赛<rt>sài</rt></ruby><ruby>开<rt>kāi</rt></ruby><ruby>始<rt>shǐ</rt></ruby><ruby>了<rt>le</rt></ruby>！<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>跑<rt>pǎo</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>很<rt>hěn</rt></ruby><ruby>快<rt>kuài</rt></ruby>，<ruby>一<rt>yī</rt></ruby><ruby>会<rt>huì</rt></ruby><ruby>儿<rt>er</rt></ruby><ruby>就<rt>jiù</rt></ruby><ruby>跑<rt>pǎo</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>很<rt>hěn</rt></ruby><ruby>远<rt>yuǎn</rt></ruby><ruby>了<rt>le</rt></ruby>。<ruby>它<rt>tā</rt></ruby><ruby>回<rt>huí</rt></ruby><ruby>头<rt>tóu</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>看<rt>kàn</rt></ruby>，<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>才<rt>cái</rt></ruby><ruby>爬<rt>pá</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>段<rt>duàn</rt></ruby><ruby>路<rt>lù</rt></ruby>。
</p>
<p>
<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>想<rt>xiǎng</rt></ruby>：<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>爬<rt>pá</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>这<rt>zhè</rt></ruby><ruby>么<rt>me</rt></ruby><ruby>慢<rt>màn</rt></ruby>，<ruby>我<rt>wǒ</rt></ruby><ruby>睡<rt>shuì</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>觉<rt>jiào</rt></ruby><ruby>也<rt>yě</rt></ruby><ruby>能<rt>néng</rt></ruby><ruby>赢<rt>yíng</rt></ruby>。<ruby>于<rt>yú</rt></ruby><ruby>是<rt>shì</rt></ruby>，<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>树<rt>shù</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>睡<rt>shuì</rt></ruby><ruby>着<rt>zháo</rt></ruby><ruby>了<rt>le</rt></ruby>。
</p>
<p>
<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>直<rt>zhí</rt></ruby><ruby>往<rt>wǎng</rt></ruby><ruby>前<rt>qián</rt></ruby><ruby>爬<rt>pá</rt></ruby>，<ruby>一<rt>yī</rt></ruby><ruby>刻<rt>kè</rt></ruby><ruby>也<rt>yě</rt></ruby><ruby>不<rt>bù</rt></ruby><ruby>停<rt>tíng</rt></ruby>。<ruby>它<rt>tā</rt></ruby><ruby>爬<rt>pá</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby>，<ruby>继<rt>jì</rt></ruby><ruby>续<rt>xù</rt></ruby><ruby>往<rt>wǎng</rt></ruby><ruby>前<rt>qián</rt></ruby><ruby>爬<rt>pá</rt></ruby>。
</p>
<p>
<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>醒<rt>xǐng</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>看<rt>kàn</rt></ruby>，<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>快<rt>kuài</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>终<rt>zhōng</rt></ruby><ruby>点<rt>diǎn</rt></ruby><ruby>了<rt>le</rt></ruby>！<ruby>兔<rt>tù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>赶<rt>gǎn</rt></ruby><ruby>紧<rt>jǐn</rt></ruby><ruby>跑<rt>pǎo</rt></ruby>，<ruby>可<rt>kě</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>已<rt>yǐ</rt></ruby><ruby>经<rt>jīng</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>不<rt>bu</rt></ruby><ruby>及<rt>jí</rt></ruby><ruby>了<rt>le</rt></ruby>。
</p>
<p>
<ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>第<rt>dì</rt></ruby><ruby>一<rt>yī</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>达<rt>dá</rt></ruby><ruby>终<rt>zhōng</rt></ruby><ruby>点<rt>diǎn</rt></ruby>，<ruby>赢<rt>yíng</rt></ruby><ruby>了<rt>le</rt></ruby>！<ruby>大<rt>dà</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>为<rt>wèi</rt></ruby><ruby>乌<rt>wū</rt></ruby><ruby>龟<rt>guī</rt></ruby><ruby>欢<rt>huān</rt></ruby><ruby>呼<rt>hū</rt></ruby>。
</p>
<p>
<ruby>这<rt>zhè</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>故<rt>gù</rt></ruby><ruby>事<rt>shì</rt></ruby><ruby>告<rt>gào</rt></ruby><ruby>诉<rt>sù</rt></ruby><ruby>我<rt>wǒ</rt></ruby><ruby>们<rt>men</rt></ruby>：<ruby>只<rt>zhǐ</rt></ruby><ruby>要<rt>yào</rt></ruby><ruby>坚<rt>jiān</rt></ruby><ruby>持<rt>chí</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>懈<rt>xiè</rt></ruby>，<ruby>就<rt>jiù</rt></ruby><ruby>能<rt>néng</rt></ruby><ruby>取<rt>qǔ</rt></ruby><ruby>得<rt>dé</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>功<rt>gōng</rt></ruby>。
</p>
"""
    }
]


def get_today_story():
    """随机获取一个故事（优先从TianAPI获取）"""
    try:
        from services.tianapi import get_random_tianapi_content
        api_story = get_random_tianapi_content()
        if api_story:
            return {
                'id': 'api',
                'title': api_story['title'],
                'image': api_story['image'],
                'content': api_story['content'],
                'type_name': api_story.get('type_name', '')
            }
    except Exception as e:
        print(f"TianAPI获取失败，使用本地故事: {e}")
    
    return random.choice(STORIES)


def get_story_by_id(story_id):
    """根据ID获取故事"""
    for story in STORIES:
        if story["id"] == story_id:
            return story
    return None


def get_random_story(exclude_ids=None):
    """获取随机本地故事"""
    if exclude_ids is None:
        exclude_ids = []
    # 只使用本地故事，不调用API
    available = [s for s in STORIES if s["id"] not in exclude_ids]
    if not available:
        available = STORIES
    return random.choice(available)


def get_all_story_ids():
    """获取所有故事ID列表"""
    return [s["id"] for s in STORIES]


