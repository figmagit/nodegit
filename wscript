import Options, Utils
from subprocess import Popen
import os
from os import system
from os.path import exists, abspath

VERSION = '0.0.1'
APPNAME = 'nodegit2'
srcdir = '.'
blddir = 'build'

def set_options(opt):
  opt.tool_options('gcc')
  opt.tool_options('compiler_cxx')

def configure(conf):
  conf.check_tool('gcc')
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')

  os.chdir('vendor/libgit2')
  Popen('python waf configure build-static', shell=True).wait()

  conf.env.append_value('LIBPATH_GIT2', abspath('build/static'))
  conf.env.append_value('LIB_GIT2', 'git2')

def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'nodegit2'
  obj.source = 'src/base.cc src/error.cc src/reference.cc src/repo.cc src/commit.cc src/oid.cc src/revwalk.cc'
  obj.rpath = abspath('build/static')
  obj.uselib = 'GIT2'