from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
    
    