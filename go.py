import os,re,shutil
from PIL import Image
# 加入循环指令控制
# 加入移除AZ区
# 回退到源图功能
# 加入备份功能


class pic:
    def __init__(self,pic_file_name,md_name):
        self.file_name=pic_file_name
        self.source_path='./{}-source-pic/{}'.format(md_name,pic_file_name)
        self.using_path='./{}-using-pic/{}'.format(md_name,pic_file_name)
        self.md_pic_source_link='![{}]({} "")'.format(pic_file_name,self.source_path)
        self.md_pic_using_link='![{}]({} "")'.format(pic_file_name,self.using_path)
    def md_pic_path_2_pic_obj(md_pic_link,md_name):
     
        pic_file_name=md_pic_link.split('(')[-1].split(' ')[0].split('/')[-1]

        return pic(pic_file_name,md_name)

       

if __name__=='__main__':


    appendzonehead='\n-----------\n## Pic Append Zone\n-----------\n'
    
    
    md_name=input('input file name:\n>')
    md_filename=md_name+'.md'

    source_pic_folder='./{}-source-pic/'.format(md_name)
    using_pic_folder='./{}-using-pic/'.format(md_name)

    print('MD+Pic 1.0.0')    
    action=input('输入操作：\n\nnp: new project\nas: append source pic\ntu: transfer using pic\nrs: resize using pic\n\n>')
    
    if action=='np':
        print('creating new project ...')
        with open(md_filename,'w'):
            pass
        os.mkdir(source_pic_folder)
        os.mkdir(using_pic_folder)
        print('Done!')

    elif action =='as':
        print('append source picture to Pic-Append-Zone ...')
        piclist=os.listdir(source_pic_folder)
        mdstr=appendzonehead
        picstr='![{}]({} "")\n\n'
        for picname in piclist:
            mdstr+=picstr.format(
                picname,
            source_pic_folder+picname
            )
        with open(md_filename,'a') as f:
            f.write(mdstr)
        print('Done!')

    elif action == 'tu':
        print('transfering using Pic to using folder ...')
        shutil.rmtree('./{}-using-pic'.format(md_name))
        os.mkdir(using_pic_folder)

        with open(md_filename) as f:
            mdtext=f.read()
        zones=mdtext.split(appendzonehead)
        pattern=re.compile(r'!\[\S+\]\(\S+ ""\)')
        using_pics=[
            pic.md_pic_path_2_pic_obj(md_pic_link,md_name) 
            for 
            md_pic_link in re.findall(pattern,zones[0])
            ]

        for using_pic in using_pics:
            print(using_pic.source_path,' -> ',using_pic.using_path)
            shutil.copyfile(using_pic.source_path,using_pic.using_path)
            zones[0]=zones[0].replace(
                using_pic.source_path,
                using_pic.using_path,
                )
        with open(md_filename,'w') as f:
            f.write(zones[0]+appendzonehead+zones[1])
        print('Done!')

    elif action == 'rs':
        print('resizeing using Pic ...')
        size=input('max size(like "600 500"):\n>').split(' ')
        size[0]=int(size[0])
        size[1]=int(size[1])
        piclist=os.listdir(using_pic_folder)
        for picname in piclist:
            im=Image.open(source_pic_folder+picname)
           
            if size[0]<im.size[0]:
                new_im=im.resize((size[0],int(size[0]/im.size[0]*im.size[1])),)
            elif size[1]<im.size[1]:
                new_im=im.resize(
                        (
                        int(size[1]/im.size[1]*im.size[0]),
                        size[1],
                        )
                    )

            print(using_pic_folder+picname)      
            print(im.size,' -> ',new_im.size)
            
            new_im.save(using_pic_folder+picname)
        print('Done!')

    else:
        print('输入有误！')