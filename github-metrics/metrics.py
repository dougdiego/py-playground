from github import Github
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
from github.GithubException import RateLimitExceededException, GithubException
from datetime import timezone

# Constants
DEBUG_REPO_LIMIT = 10
SORT_DIRECTION = 'desc'  # 'asc' for oldest first, 'desc' for newest first

def count_lines_of_code(repo):
    """Count lines of code in the repository."""
    try:
        stats = repo.get_stats_code_frequency()
        if stats:
            total_additions = sum(stat.additions or 0 for stat in stats)
            total_deletions = abs(sum(stat.deletions or 0 for stat in stats))
            return {
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'net_lines': total_additions - total_deletions
            }
    except Exception as e:
        print(f"Error getting code frequency stats: {str(e)}")
    return None

def get_org_metrics(org_name, token, year=2024, debug=False, repo_name=None):
    g = Github(token)
    try:
        # Check rate limit before starting
        rate_limit = g.get_rate_limit()
        if rate_limit.core.remaining < 100:
            raise Exception(f"Rate limit too low: {rate_limit.core.remaining} remaining")
            
        org = g.get_organization(org_name)
        
        metrics = {
            'repo_count': 0,
            'total_commits': 0,
            'total_prs': 0,
            'languages': set(),
            'contributors': set(),
            'code_frequency': {
                'additions': 0,
                'deletions': 0,
                'net_lines': 0
            },
            'lines_of_code': {
                'total_additions': 0,
                'total_deletions': 0,
                'net_lines': 0
            }
        }
        
        # Create timezone-aware datetime objects
        start_date = datetime(year, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        
        # Get repositories based on input parameters
        all_repos = []
        try:
            print(f"Attempting to fetch repositories for organization: {org_name}")
            
            if repo_name:
                # Get single repository
                try:
                    repo = org.get_repo(repo_name)
                    all_repos = [repo]
                    print(f"Found repository: {repo.name} (Private: {repo.private})")
                except Exception as e:
                    print(f"Error: Repository {repo_name} not found or not accessible")
                    raise e
            else:
                # Get all repositories
                repos_iterator = org.get_repos(sort='created', direction=SORT_DIRECTION, type='private')
                print("Successfully created repository iterator")
                
                for repo in repos_iterator:
                    print(f"Found repository: {repo.name} (Private: {repo.private})")
                    all_repos.append(repo)
                    if len(all_repos) % 10 == 0:
                        print(f"Fetched {len(all_repos)} repositories so far...")
        
        except Exception as e:
            print(f"Warning: Error while fetching repositories: {str(e)}")
            print(f"Error type: {type(e)}")
        
        print(f"Total repositories fetched: {len(all_repos)}")
        
        repos = all_repos
        if debug and not repo_name:  # Only apply debug limit if not processing specific repo
            message = "most recent" if SORT_DIRECTION == 'desc' else "oldest"
            print(f"DEBUG MODE: Processing only {message} {DEBUG_REPO_LIMIT} repositories")
            repos = repos[:DEBUG_REPO_LIMIT]
        
        for repo in repos:
            print(f"Processing repository: {repo.name}")
            metrics['repo_count'] += 1
            
            try:
                # Get language stats
                metrics['languages'].update(repo.get_languages().keys())
                
                # Get commits for the year (with pagination)
                commits = repo.get_commits(since=start_date, until=end_date)
                for commit in commits:
                    metrics['total_commits'] += 1
                    if commit.author:
                        metrics['contributors'].add(commit.author.login)
                
                # Get PRs for the year (with pagination)
                prs = repo.get_pulls(state='all', sort='created', direction='desc')
                for pr in prs:
                    if start_date <= pr.created_at <= end_date:
                        metrics['total_prs'] += 1
                    elif pr.created_at < start_date:
                        break

                # Get lines of code stats
                loc_stats = count_lines_of_code(repo)
                if loc_stats:
                    metrics['lines_of_code']['total_additions'] += loc_stats['total_additions']
                    metrics['lines_of_code']['total_deletions'] += loc_stats['total_deletions']
                    metrics['lines_of_code']['net_lines'] += loc_stats['net_lines']
                        
            except RateLimitExceededException:
                print("Rate limit exceeded. Saving partial results...")
                break
            except Exception as e:
                print(f"Error processing repo {repo.name}: {str(e)}")
                continue
        
        # Convert sets to lists for JSON serialization
        metrics['languages'] = list(metrics['languages'])
        metrics['contributors'] = list(metrics['contributors'])
        
        return metrics
    finally:
        g.close()

def main():
    # Load environment variables
    load_dotenv()
    
    # Get token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN not found in environment variables")
    
    # Set organization name
    org_name = "prosperllc"
    
    # Get debug mode from environment, defaults to False
    debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Get optional repository name from environment
    repo_name = os.getenv('REPO')
    
    try:
        # Get metrics with debug flag and optional repo name
        metrics = get_org_metrics(org_name, token, debug=debug_mode, repo_name=repo_name)
        
        # Save to JSON file
        output_file = 'output.json'
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Set restrictive permissions on output file
        os.chmod(output_file, 0o600)
        
        print(f"Metrics successfully saved to {output_file}")
        if debug_mode and not repo_name:
            print(f"Note: Results are from debug mode (limited to {DEBUG_REPO_LIMIT} repositories)")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()