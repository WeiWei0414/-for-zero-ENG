import os
from pydub import AudioSegment
import re
from pydub.silence import detect_silence
from pydub.silence import detect_nonsilent
def split_audio_man_women(input_file, silence_thresh=-40, min_silence_len=1000, buffer_ms=50):
 
    # 加載音頻文件
    audio = AudioSegment.from_file(input_file)
    print(f"成功加載音頻文件: {input_file}")
    
    # 檢測靜音段位置
    silence_ranges = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    # 調整靜音段範圍為切割點
    cut_points = [0] + [end - buffer_ms for start, end in silence_ranges if end - buffer_ms > 0] + [len(audio)] 
    # 切割音頻
    segments = [audio[start:end] for start, end in zip(cut_points[:-1], cut_points[1:])]
    return segments
def combine_audio_segments_manAndWomen(female_segments, male_segments, output_folder):
  
    os.makedirs(output_folder, exist_ok=True)
    
    combined_files = []
    for i, (female_seg, male_seg) in enumerate(zip(female_segments, male_segments)):
        # 組合：女 + 男 + 女 + 男
        combined = female_seg + male_seg + female_seg + male_seg
        
        # 保存文件
        output_path = os.path.join(output_folder, f"segment_{i + 1}.wav")
        combined.export(output_path, format="wav")
        combined_files.append(output_path)
        print(f"輸出: {output_path}")
    


def split_audio(input_file, output_folder, silence_thresh=-40, min_silence_len=1000, buffer_ms=50):

    # 加載音頻文件
    audio = AudioSegment.from_file(input_file)
    print(f"成功加載音頻文件: {input_file}")
    
    # 檢測靜音段位置
    silence_ranges = detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    # 調整靜音段範圍為切割點
    cut_points = [0] + [end - buffer_ms for start, end in silence_ranges if end - buffer_ms > 0] + [len(audio)]
    
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 切割音頻並保存
    for i in range(len(cut_points) - 2):
        start = cut_points[i]
        end = cut_points[i + 1]
        segment = audio[start:end]
        output_path = os.path.join(output_folder, f"segment_{i+1}.wav")
        segment.export(output_path, format="wav")
        print(f"輸出: {output_path}")
def split_slow_audio(input_file, output_folder, silence_thresh=-40, min_silence_len=500, buffer_ms=50, min_gap=1000, max_gap=1500):
    
    # 加載音頻文件
    audio = AudioSegment.from_file(input_file)
    print(f"成功加載音頻文件: {input_file}")

    # 檢測非靜音段落
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    # 儲存切割片段的時間點
    cut_points = [0]  # 起始點
    for i in range(len(nonsilent_ranges) - 1):
        _, end_current = nonsilent_ranges[i]
        start_next, _ = nonsilent_ranges[i + 1]

        # 計算相鄰聲音之間的間隔
        gap = start_next - end_current

        if gap >= max_gap:
            # 當間隔大於最大間隔時，切割點在下一段聲音的開始前50ms
            cut_points.append(max(0, start_next - buffer_ms))
        elif gap < min_gap:
            # 當間隔小於最小間隔時，將段落合併（不切割）
            continue

    cut_points.append(len(audio))  # 添加結束點

    # 根據切割點生成片段
    segments = [audio[start:end] for start, end in zip(cut_points[:-1], cut_points[1:])]

    # 保存切割片段
    for i, segment in enumerate(segments):
        output_path = os.path.join(output_folder, f"segment_{i + 1}.wav")
        segment.export(output_path, format="wav")

def sort_files_by_number(files):
    """
    根據文件名中的數字對文件列表進行排序。
    :param files: 文件名列表
    :return: 排序後的文件名列表
    """
    return sorted(files, key=lambda x: int(re.search(r"(\d+)", x).group(1)))

def combine_files_from_folders(folder_list, output_file):
    """
    按照規則從多個文件夾中取文件，並合併為一個音頻文件。
    
    :param folder_list: 資料夾列表，每個資料夾包含切割後的音頻文件
    :param output_file: 輸出的合併音頻文件路徑
    """
    combined_audio = AudioSegment.empty()
    folder_pointers = {folder: 0 for folder in folder_list}  # 每個文件夾的當前處理指針

    while True:
        has_files = False

        # 遍歷每個文件夾
        for folder in folder_list:
            if folder not in folder_pointers:
                continue

            # 特殊處理 folder_5
            if folder == "folder_5":
                for _ in range(3):  # 從 folder_5 取 3 個音頻文件
                    if folder_pointers[folder] < len(folder_list[folder]):
                        file = folder_list[folder][folder_pointers[folder]]
                        file_path = os.path.join(folder, file)
                        print(f"  合併音頻 (folder_5): {file_path}")
                        combined_audio += AudioSegment.from_file(file_path)
                        folder_pointers[folder] += 1
                        has_files = True
                continue  # 處理完 folder_5 後，直接跳到下一個文件夾

            # 處理其他文件夾
            elif folder_pointers[folder] < len(folder_list[folder]):
                file = folder_list[folder][folder_pointers[folder]]
                file_path = os.path.join(folder, file)
                print(f"  合併音頻: {file_path}")
                combined_audio += AudioSegment.from_file(file_path)
                folder_pointers[folder] += 1
                has_files = True

        # 如果所有文件夾都處理完畢，退出循環
        if not has_files:
            break

    # 將合併後的音頻導出為 MP3 文件
    combined_audio.export(output_file, format="mp3")
    print(f"合併完成，輸出文件: {output_file}")


if __name__ == "__main__":
    #女生
    file_name='女2s.mp3'
    output_folder='folder_1' 
    if not os.path.exists(file_name):
        print(f"Error: {file_name} audio files are missing. 請確認")
        exit()
    split_audio(file_name,output_folder)
    #男生
    file_name='男2s.mp3'
    output_folder='folder_2' 
    if not os.path.exists(file_name):
        print(f"Error: {file_name} audio files are missing. 請確認")
        exit()
    split_audio(file_name,output_folder)
    #中文
    file_name='中文.mp3'
    output_folder='folder_3' 
    if not os.path.exists(file_name) :
        print(f"Error: {file_name} audio files are missing. 請確認")
        exit()
    split_audio(file_name,output_folder)
    #慢速版
    file_name = "慢速版.mp3"
    output_folder = "folder_4"
    if not os.path.exists(file_name):
            print(f"Error: {file_name} audio files are missing. 請確認")
            exit()
    os.makedirs(output_folder, exist_ok=True)
    split_slow_audio(file_name, output_folder)
    #分解版
    female_mp3 = "分解版女.mp3"  # 女聲音頻文件
    male_mp3 = "分解版男.mp3"      # 男聲音頻文件
    if not os.path.exists(female_mp3) or not os.path.exists(male_mp3):
        print("Error: One or both audio files are missing.")
        exit() 
    female_segments = split_audio_man_women(female_mp3)
    male_segments = split_audio_man_women(male_mp3)
    # 確保片段數量相等
    min_segments = min(len(female_segments), len(male_segments))
    female_segments = female_segments[:min_segments]
    male_segments = male_segments[:min_segments]
    output_folder = "folder_5"
    combine_audio_segments_manAndWomen(female_segments, male_segments, output_folder)
    #女4s
    file_name='女4s.mp3'
    output_folder='folder_6' 
    if not os.path.exists(file_name):
        print(f"Error: {file_name} audio files are missing. 請確認")
        exit()
    split_audio(file_name,output_folder)

    file_name='男4s.mp3'
    output_folder='folder_7' 
    if not os.path.exists(file_name):
        print(f"Error: {file_name} audio files are missing. 請確認")
        exit()
    split_audio(file_name,output_folder)

        # 定義文件夾
    folder_list = [
        "folder_1",
        "folder_2",
        "folder_3",
        "folder_4",
        "folder_5",
        "folder_6",
        "folder_7",
    ]
    # 文件夾中的文件名列表（按順序排序）
    folder_files = {folder: sort_files_by_number(os.listdir(folder)) for folder in folder_list}

    # 輸出文件
    output_file = "final_combined.mp3"

    # 執行合併
    combine_files_from_folders(folder_files, output_file)