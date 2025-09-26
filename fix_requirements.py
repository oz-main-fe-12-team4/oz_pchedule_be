# fix_requirements.py
input_file = "requirements.txt"  # 현재 폴더 기준
output_file = "requirements_fixed.txt"  # 같은 폴더에 생성

with open(input_file, "r") as f:
    lines = f.readlines()

fixed_lines = []
for line in lines:
    line = line.strip()
    if not line:
        continue  # 빈 줄 제거
    if line.startswith("#"):
        fixed_lines.append(line)
        continue
    if "==" in line:
        pkg, ver = line.split("==", 1)
        if not ver.strip():
            # 버전이 비어있으면 제거
            fixed_lines.append(pkg)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open(output_file, "w") as f:
    f.write("\n".join(fixed_lines))

print(f"수정 완료: {output_file}")
