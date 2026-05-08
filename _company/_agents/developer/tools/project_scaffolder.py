import os
import subprocess
import argparse

def scaffold_project(project_name, template="next"):
    """
    1인 기업 OS - Developer Agent용 프로젝트 스캐폴더
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../projects"))
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    target_dir = os.path.join(base_dir, project_name)
    
    if os.path.exists(target_dir):
        print(f"❌ 오류: 이미 '{project_name}' 프로젝트가 존재합니다.")
        return False
        
    print(f"🚀 '{project_name}' 프로젝트 스캐폴딩 시작... (템플릿: {template})")
    
    try:
        if template == "next":
            # Next.js App Router, Tailwind, TypeScript (Non-interactive)
            cmd = f"npx -y create-next-app@latest {target_dir} --ts --tailwind --eslint --app --src-dir --import-alias '@/*'"
        elif template == "vite":
            # Vite + React + TS
            cmd = f"npx -y create-vite@latest {target_dir} --template react-ts"
        else:
            print("❌ 지원하지 않는 템플릿입니다. (next 또는 vite)")
            return False
            
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ 프로젝트 생성 완료: {target_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 프로젝트 생성 실패: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="프로젝트 자동 스캐폴더")
    parser.add_argument("name", help="생성할 프로젝트 이름")
    parser.add_argument("--template", default="next", choices=["next", "vite", "astro"], help="사용할 프레임워크 템플릿")
    
    args = parser.parse_args()
    scaffold_project(args.name, args.template)
