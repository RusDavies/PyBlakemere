#!/bin/bash


repos=(	"git@github.com:RusDavies/PyAutoWrapper.git", \
	"git@github.com:RusDavies/PyGitHubMapper.git", \
	"git@github.com:RusDavies/PyLog4JAnalysis.git", \
	"git@github.com:RusDavies/RusPyJira.git", \
	"git@github.com:RusDavies/RusPySparx.git" )

for url in ${repos[@]}; do
  reponame=${url##*/}
  folder=${reponame%.*}
  if [ ! -e "${folder}" ]; then
    printf "Adding ${url} as ${folder}\n"
    git submodule add "${url}" "${folder}"
  fi

done

