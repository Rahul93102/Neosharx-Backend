from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Startup Stories endpoints
    path('stories/', views.list_startup_stories, name='list_startup_stories'),
    path('stories/featured/', views.get_featured_story, name='get_featured_story'),
    path('stories/filters/', views.get_story_filters, name='get_story_filters'),
    path('stories/<slug:slug>/', views.get_startup_story, name='get_startup_story'),
    # Neo Stories endpoints
    path('neo-stories/', views.list_neo_stories, name='list_neo_stories'),
    path('neo-stories/featured/', views.get_featured_neo_story, name='get_featured_neo_story'),
    path('neo-stories/filters/', views.get_neo_story_filters, name='get_neo_story_filters'),
    path('neo-stories/<slug:slug>/', views.get_neo_story, name='get_neo_story'),
    # Neo Projects endpoints
    path('neo-projects/', views.list_neo_projects, name='list_neo_projects'),
    path('neo-projects/featured/', views.get_featured_neo_projects, name='get_featured_neo_projects'),
    path('neo-projects/filters/', views.get_neo_project_filters, name='get_neo_project_filters'),
    path('neo-projects/<slug:slug>/', views.get_neo_project, name='get_neo_project'),
    path('neo-projects/<slug:slug>/full/', views.get_neo_project_detail, name='get_neo_project_detail'),
    # SharXathon (Hackathon) endpoints
    path('hackathons/', views.get_sharxathons, name='get_sharxathons'),
    path('hackathons/featured/', views.get_featured_sharxathons, name='get_featured_sharxathons'),
    path('hackathons/upcoming/', views.get_upcoming_sharxathons, name='get_upcoming_sharxathons'),
    path('hackathons/filters/', views.get_sharxathon_filters, name='get_sharxathon_filters'),
    path('hackathons/<slug:slug>/', views.get_sharxathon_detail, name='get_sharxathon_detail'),
    path('hackathons/<slug:slug>/countdown/', views.get_sharxathon_countdown, name='get_sharxathon_countdown'),
    # Tech News endpoints
    path('tech-news/', views.get_tech_news, name='get_tech_news'),
    path('tech-news/featured/', views.get_featured_tech_news, name='get_featured_tech_news'),
    path('tech-news/breaking/', views.get_breaking_tech_news, name='get_breaking_tech_news'),
    path('tech-news/trending/', views.get_trending_tech_news, name='get_trending_tech_news'),
    path('tech-news/categories/', views.get_tech_news_categories, name='get_tech_news_categories'),
    path('tech-news/<slug:slug>/', views.get_tech_news_detail, name='get_tech_news_detail'),
    path('tech-news/<slug:slug>/like/', views.like_tech_news, name='like_tech_news'),
    path('tech-news/<slug:slug>/share/', views.share_tech_news, name='share_tech_news'),
    
    # Talk Episodes endpoints
    path('talk-episodes/', views.talk_episodes_list, name='talk_episodes_list'),
    path('talk-episodes/slug/<slug:slug>/', views.talk_episode_detail, name='talk_episode_detail'),
    path('talk-episodes/number/<int:episode_number>/', views.talk_episode_by_number, name='talk_episode_by_number'),
    
    # Robotics News endpoints
    path('robotics-news/', views.get_robotics_news, name='get_robotics_news'),
    path('robotics-news/featured/', views.get_featured_robotics_news, name='get_featured_robotics_news'),
    path('robotics-news/trending/', views.get_trending_robotics_news, name='get_trending_robotics_news'),
    path('robotics-news/<slug:slug>/', views.get_robotics_news_detail, name='get_robotics_news_detail'),
    path('robotics-news/<slug:slug>/like/', views.like_robotics_news, name='like_robotics_news'),
    path('robotics-news/<slug:slug>/share/', views.share_robotics_news, name='share_robotics_news'),
    
    # Comment System endpoints
    path('comments/', views.comments_list_create, name='comments_list_create'),
    path('comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('comments/like/', views.comment_like_toggle, name='comment_like_toggle'),
    path('comments/<int:comment_id>/flag/', views.comment_flag, name='comment_flag'),
    path('comments/user/', views.user_comments, name='user_comments'),
    path('comments/admin/flagged/', views.admin_flagged_comments, name='admin_flagged_comments'),
    
    # Event endpoints
    path('events/', views.events_list_create, name='events_list_create'),
    path('events/type/<str:event_type>/', views.events_by_type, name='events_by_type'),
    path('events/featured/', views.events_featured, name='events_featured'),
    path('events/categories/', views.events_categories, name='events_categories'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    
    # YouTube Video endpoints
    path('youtube-videos/', views.youtube_videos_list, name='youtube_videos_list'),
    path('youtube-videos/featured/', views.youtube_videos_featured, name='youtube_videos_featured'),
    path('youtube-videos/type/<str:video_type>/', views.youtube_videos_by_type, name='youtube_videos_by_type'),
    path('youtube-videos/<slug:slug>/', views.youtube_video_detail, name='youtube_video_detail'),
    
    # User Preferences endpoint
    path('user-preferences/', views.user_preferences, name='user_preferences'),
    
    # OAuth endpoints
    path('google/login-url/', views.google_login_url, name='google_login_url'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('linkedin/login-url/', views.linkedin_login_url, name='linkedin_login_url'),
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),
]