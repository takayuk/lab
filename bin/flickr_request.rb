# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

require 'open-uri'
require 'rexml/document'
require 'cgi'


FLICKR_API_KEY = '462f636d0921ef211d8dbc676d1538b2'
HTTP_PROXY = 'http://cache.st.ryukoku.ac.jp:8080/'


#
# リクエストURIの生成.
#
def new_request(method_name, arg_map = {}.freeze)
	begin
		args = arg_map.collect{|k, v| CGI.escape(k) << '=' << CGI.escape(v)}.join('&')

		request_url = "http://www.flickr.com/services/rest/?api_key=%s&method=%s&%s" %
		[FLICKR_API_KEY, method_name, args]

		return REXML::Document.new(open(request_url, :proxy=>HTTP_PROXY))
	rescue

		STDERR.puts "LOCAL WARNINGS: #{$!}"
		return nil
	end
end


def photos_geobbox(bbox)

  @bbox_argstr = bbox.values.join(',').freeze

  @response = new_request(
    'flickr.photos.search', 'has_geo'=>'1', 'perpage'=>'500',
    'bbox'=>@bbox_argstr).freeze

  return if @response.nil?
  if @response.elements['rsp/'].attributes['stat'] == 'fail'
    puts(@response.elements['rsp/err/'].attributes['msg'])
    return
  end

  @pages = @response.elements['rsp/photos/'].attributes['pages'].to_i.freeze

  @photos = []
  for page in 1..@pages

    @response = new_request(
      'flickr.photos.search', 'has_geo'=>'1', 'page'=>page.to_s, 'perpage'=>'500',
      'bbox'=>@bbox_argstr
    )

    @response.elements.each('rsp/photos/photo/') do |photo|
      @photos << photo.attributes['id']
    end
  end

  @photos.freeze
end


if __FILE__ == $0

  puts("started...")

  sample_bbox = {
    :minlon=>"134.208984",:minlat=>"33.300275",
    :maxlon=>"141.525879",:maxlat=>"37.330528"
  }.freeze
 
  result = photos_geobbox(sample_bbox)

  puts(result.size)

  puts("done...")
end

