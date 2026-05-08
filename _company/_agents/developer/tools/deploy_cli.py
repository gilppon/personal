import os
import subprocess
import argparse

def deploy_project(project_name, platform="vercel", prod=False):
    """
    1인 기업 OS - Developer Agent용 배포 CLI (deploy_cli)
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../projects"))
    target_dir = os.path.join(base_dir, project_name)
    
    if not os.path.exists(target_dir):
        print(f"❌ 오류: '{project_name}' 프로젝트를 찾을 수 없습니다. 경로: {target_dir}")
        return False
        
    print(f"🚀 '{project_name}' 프로젝트 배포 준비 중... (플랫폼: {platform}, 모드: {'운영(PROD)' if prod else '미리보기(Preview)'})")
    
    try:
        if platform == "vercel":
            # Vercel 배포 명령어
            cmd = "npx vercel"
            if prod:
                cmd += " --prod"
        elif platform == "cloudflare":
            # Cloudflare Pages 배포 명령어 (폴더명이 out이나 dist라고 가정)
            # 프로젝트에 따라 빌드 폴더가 다를 수 있음
            build_folder = "dist" if os.path.exists(os.path.join(target_dir, "dist")) else ".next"
            cmd = f"npx wrangler pages deploy {build_folder} --project-name {project_name}"
            # Cloudflare는 branch 이름 등으로 prod 관리
        else:
            print("❌ 지원하지 않는 플랫폼입니다. (vercel 또는 cloudflare)")
            return False
            
        print(f"⚙️ 실행 명령어: {cmd}")
        print("-" * 40)
        # 해당 프로젝트 폴더로 이동하여 명령어 실행
        subprocess.run(cmd, shell=True, check=True, cwd=target_dir)
        print("-" * 40)
        print(f"✅ 배포 완료!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 배포 실패: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="프로젝트 자동 배포 CLI")
    parser.add_argument("name", help="배포할 프로젝트 이름")
    parser.add_argument("--platform", default="vercel", choices=["vercel", "cloudflare"], help="배포할 플랫폼")
    parser.add_argument("--prod", action="store_true", help="운영(Production) 환경에 배포 (기본은 Preview)")
    
    args = parser.parse_args()
    
    # 보안 승인 게이트 (tools.md 규칙: 운영 배포는 항상 경고)
    if args.prod:
        print("⚠️ [경고] 운영(PROD) 환경 배포가 요청되었습니다.")
        print("보안 규칙에 따라 CEO(사용자)의 최종 승인이 필요합니다.")
        confirm = input("배포를 진행하시겠습니까? (y/N): ")
        if confirm.lower() != 'y':
            print("🛑 배포가 취소되었습니다.")
            exit(0)
            
    deploy_project(args.name, args.platform, args.prod)
