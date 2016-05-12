# Intended to work on Ubuntu 12.04

package "binutils" do
    :upgrade
end

package "gdal-bin" do
    :upgrade
end

package "libproj-dev" do
    :upgrade
end

package "postgresql-9.3" do
    :upgrade
end

package "postgresql-server-dev-all" do
    :upgrade
end

package "python-psycopg2" do
    :upgrade
end

# Set a virtual host file for each app
template "/etc/postgresql/9.3/main/pg_hba.conf" do
  source "postgresql/pg_hba.erb"
  mode 0640
  owner "root"
  group "root"
  variables({
     :db_user => node[:app][:db_user]
  })
end
