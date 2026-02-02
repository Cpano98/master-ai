# Serve static HTML portfolio with nginx
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY minimal-personal-portfolio-html-template-master/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]