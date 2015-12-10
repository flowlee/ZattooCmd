#!/usr/bin/env python 
# -*- coding: utf-8 -*-  

from zapisession import ZapiSession
import sys
import argparse

class Main(object):
  z = None
  # FIXME, add Zattoo Login here!
  ZattooUser = ''
  ZattooPass = ''
  ChannelList = None
  
  def __init__(self):
    self.z = ZapiSession('/tmp/')
    self.z.init_session(self.ZattooUser, self.ZattooPass)
  
  def login(self):
    if self.z.login():
        print ("Login ok")
    else:
        print ("Login not ok...")
        sys.exit(0)
    self.z.announce()
    ChannelList = self.retrieve_channels()
  
    
  def retrieve_channels(self):
    api = '/zapi/v2/cached/channels/%s?details=False' % self.z.AccountData['account']['power_guide_hash']
    channelsData = self.z.exec_zapiCall(api, None)
    if channelsData is not None:
      #if inst.CACHE_ENABLED:
          #inst.persist_channels(channelsData)
      return channelsData
    return None

  def get_allChannels(self, flag_favorites=False):
    channelsData = self.retrieve_channels()
    if channelsData is None:
      return None

    if flag_favorites:
      api = '/zapi/channels/favorites'
      favoritesData = self.ZapiSession.exec_zapiCall(api, None)
      if favoritesData is None:
        return None

    allChannels = []
    for group in channelsData['channel_groups']:
      for channel in group['channels']:
        allChannels.append({
          'id': channel['id'],
          'title': channel['title'],
           #  'image_url': self.fetch_imageUrl(channel['qualities'][0]['logo_black_84']),
          'recommend': 1 if channel['recommendations'] == True else 0,
          'favorite': 1 if flag_favorites and channel['id'] in favoritesData['favorites'] else 0})
    return allChannels

  def watch(self, args):
    params = {'cid': args['id'], 'stream_type': 'hls'}
    resultData = self.z.exec_zapiCall('/zapi/watch', params)
    if resultData is not None:
            url = resultData['stream']['watch_urls'][0]['url']
    return resultData

def getParser():
  parser = argparse.ArgumentParser(prog='zattooCmd', usage='%(prog)s [options]')
  parser.add_argument('-watch', help='Get URL of this channel')
  parser.add_argument('-getchannels', action="store_true", help='Get a list with includes every Zattoo channel')
  return parser
  
if __name__ == "__main__":
  p = getParser()
  args = p.parse_args()
  
  m = Main()
  m.login()
  c = m.get_allChannels()  

  if args.getchannels:
    for i in c:
      print unicode(i['title'] + ' id \t "' + i['id'] + '"').encode('utf-8')    
  elif args.watch:
    for i in c:
      if i['id'] == args.watch:
        print m.watch(i)
        break
  else:
    p.print_help()
