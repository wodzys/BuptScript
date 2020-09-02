require 'net/http'
require 'timeout'
require 'cgi'

$username = '2018140138'
# $password = '12130014'
$classes = [
    {
        'id' => '3111100488',
        'name' => '网络搜索引擎原理',
        'choose' => false
    },
    {
        'id' => '3111101166',
        'name' => '创业与创新方法论',
        'choose' => false
    },
    {
        'id' => '3311100332',
        'name' => '漫画创意与艺术欣赏（人文艺术类）',
        'choose' => false
    },
    {
        'id' => '3121400337',
        'name' => '工程计算方法',
        'choose' => false
    },
    {
        'id' => '3111400023',
        'name' => 'Web搜索',
        'choose' => false
    }
]

def try_choose(http, token, cls)
  
  return if cls["choose"] || cls["eid"].nil?
  
  puts "#{Time.now} try choose #{cls["name"]}"

  cls_response = http.request_get("/Gstudent/Course/PlanSelClass.aspx?EID=#{cls["eid"]}&UID=#{$username}", {'cookie' => token + '; DropDownListXqu=DropDownListXqu=', 'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'})
  view_state = CGI.escape(/"__VIEWSTATE" value="(.*)"/.match(cls_response.body)[1])
  evt_valid = CGI.escape(/"__EVENTVALIDATION" value="(.*)"/.match(cls_response.body)[1])

  cls_response.body.scan(/<input type="image" name=".+?"/).each do |cls_btn|
    cid = /name="(.+?)"/.match(cls_btn)[1]
    choose_response = http.request_post("/Gstudent/Course/PlanSelClass.aspx?EID=#{cls["eid"]}&UID=#{$username}", "ctl00$ScriptManager1=ctl00$contentParent$UpdatePanel2|#{cid}&ctl00$contentParent$drpXqu$drpXqu=&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=#{view_state}&__EVENTVALIDATION=#{evt_valid}&__VIEWSTATEENCRYPTED=&__ASYNCPOST=true&#{cid}.x=14&#{cid}.y=9", {'cookie' => token + '; DropDownListXqu=DropDownListXqu=', 'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0', 'Content-Type' => 'application/x-www-form-urlencoded; charset=utf-8'})
    if choose_response.body.include?('|frameElement.api.close();|')
      cls["choose"] = true
      puts "#{Time.now} #{cls["name"]} is chosen"
    else
      puts "#{Time.now} try next"
    end

    sleep 0.1
  end
end

while true do
  begin
    redir_url = ''

    Net::HTTP.start('auth.bupt.edu.cn', 80) do |http|
      http.read_timeout = 5
      http.open_timeout = 5

      login_response = http.request_get('/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx')
      jsession_id = 'JSESSIONID=' + /JSESSIONID=(.*?);/m.match(login_response.header["set-cookie"])[1]
      t_lt = /name="lt" value="(.*?)"/m.match(login_response.body)[1]
      t_exec = /name="execution" value="(.*?)"/m.match(login_response.body)[1]

      auth_response = http.request_post('/authserver/login?service=http%3a%2f%2fyjxt.bupt.edu.cn%2fULogin.aspx', "username=#{$username}&password=#{$password}&lt=#{t_lt}&execution=#{t_exec}&_eventId=submit&rmShown=1", {'cookie' => jsession_id})
      redir_url = auth_response.header["location"].gsub('http://yjxt.bupt.edu.cn', '')
    end

    puts "#{Time.now} redirect to #{redir_url}"

    if redir_url.length > 1
      Net::HTTP.start('yjxt.bupt.edu.cn', 80) do |http|
        login_response = http.request_get(redir_url)
        sesson_id = 'ASP.NET_SessionId=' + /ASP\.NET_SessionId=(.*?);/m.match(login_response.header["set-cookie"])[1]

        puts "#{Time.now} yjxt token: #{sesson_id}"

        class_response = http.request_get("/Gstudent/Course/PlanCourseOnlineSel.aspx?EID=9kWb0OKGTBF2KzmBt5QNDZLXYu1Fldi6xwxV6Yb1wPA1TrsnKBRXgg==&UID=#{$username}", {'cookie' => sesson_id})
        $classes.each do |cls|
          cls_info = Regexp.new("#{cls["id"]}(.+?)</tr>", Regexp::MULTILINE).match(class_response.body)
          if cls_info
            if (cls_info[1].include?("selClass("))
              cls["eid"] = /\?EID=(.+?)&amp;/m.match(cls_info[1])[1]
            else
              puts "#{Time.now} no room left in #{cls["name"]}"
            end
          end
        end

        $classes.each do |cls|
          try_choose(http, sesson_id, cls)

          sleep 0.1
        end 
      end
    end

    sleep 5
  rescue StandardError => msg
    p msg
    retry
  end
end
