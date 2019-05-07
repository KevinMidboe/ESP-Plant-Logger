from watercontent import watercontent
from elasticLog import logger

def main():
  print('main loaded')
  try:
    watercontent()
  except Exception as e:
    print(e)
    logger('Error thrown', {'message': 'Error thrown', 'error': e})
    print('starting again')
    watercontent()

if __name__ == '__main__':
  main()