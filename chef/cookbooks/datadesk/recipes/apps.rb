# Create the apps directory where everything will go
directory "/apps/" do
    owner node[:apps_user]
    group node[:apps_group]
    mode 0775
end

# Load the authorized keys for the root user
directory "/home/#{node[:apps_user]}/.ssh" do
  mode 0700
  owner node[:apps_user]
  group node[:apps_group]
end

cookbook_file "/home/#{node[:apps_user]}/.ssh/authorized_keys" do
  source "users/authorized_keys"
  mode 0640
  owner node[:apps_user]
  group node[:apps_group]
end

# Load the SSH keys
cookbook_file "/home/#{node[:apps_user]}/.ssh/id_rsa" do
  source "users/id_rsa"
  mode 0600
  owner node[:apps_user]
  group node[:apps_group]
end

cookbook_file "/home/#{node[:apps_user]}/.ssh/id_rsa.pub" do
  source "users/id_rsa.pub"
  mode 0644
  owner node[:apps_user]
  group node[:apps_group]
end

# Install the virtualenv requirements
script "Add GitHub to known hosts" do
  interpreter "bash"
  user node[:apps_user]
  group node[:apps_group]
  code <<-EOH
    echo "|1|nFPVjT+tJlghvwL9SqJmckclSkI=|5HR4LAIxnl3I3cl40j5GIy+Qbwk= ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" >> /home/#{node[:apps_user]}/.ssh/known_hosts
    echo "|1|LiSuPv5jaL9TCd9Tgue5BiGAJtE=|KYW9Uqo+gzE+Z3O/0uE8d9kadm0= ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" >> /home/#{node[:apps_user]}/.ssh/known_hosts
  EOH
end

# Make the directory for the app
virtualenv "/apps/#{node[:app][:name]}" do
    owner node[:apps_user]
    group node[:apps_group]
    mode 0775
end

# Make the directory for the repo
directory "/apps/#{node[:app][:name]}/repo" do
    owner node[:apps_user]
    group node[:apps_group]
    mode 0775
end

# Pull the git repo
git "/apps/#{node[:app][:name]}/repo"  do
  repository node[:app][:repo]
  reference "HEAD"
  revision node[:app][:branch]
  user node[:apps_user]
  group node[:apps_group]
  action :sync
end

# Install the virtualenv requirements
script "Install Requirements" do
  interpreter "bash"
  user node[:apps_user]
  group node[:apps_group]
  code "/apps/#{node[:app][:name]}/bin/pip install -r /apps/#{node[:app][:name]}/repo/requirements.txt"
end

# Run any management commands
node[:app][:management].each do |command|
  script "Running #{command}" do
    interpreter "bash"
    user node[:apps_user]
    code <<-EOH
      cd /apps/#{node[:app][:name]} && . bin/activate && cd repo && /apps/#{node[:app][:name]}/bin/python /apps/#{node[:app][:name]}/repo/manage.py #{command}
    EOH
  end
end
