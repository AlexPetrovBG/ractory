try:
    from app.routers import auth
    print('Auth module imported successfully')
except Exception as e:
    print(f'Error importing auth: {e}')
