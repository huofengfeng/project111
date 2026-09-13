function s(t){return t?t.startsWith("http://")||t.startsWith("https://")?t:t.startsWith("/")?"http://localhost:9090"+t:t:""}export{s as g};
