
import argparse
import os
from pathlib import Path

from fuzzer_cov.core.container import BuildContainerImpl

from fuzzer_cov.core import Logger
from fuzzer_cov.core.logger import LoggerImpl

from fuzzer_cov.core import FuzzerExecutor
from fuzzer_cov.executor.libfuzzer import LibFuzzerInstanceExecutor

from fuzzer_cov.core import CommandExecutor
from fuzzer_cov.platform.executor import CommandExecutorImpl

from fuzzer_cov.platform.lcov import LCovRunner, LCovOutputPathPolicy
from fuzzer_cov.platform.genhtml import GenHtmlRunner, GenHtmlOutputPathPolicy

class InvalidOpts(Exception): pass

class Opts(object):
    fuzzer_path: str
    source_dir: str
    output_dir: str
    lcov_output_dir: str
    gen_html_output_dir: str
    enable_branch_coverage: bool
    lcov_follow_links: bool
    lcov_exclude_pattern: str
    lcov_path: str
    gen_html_path: str

    def __init__(self):
        self.lcov_path = 'lcov'
        self.gen_html_path = 'genhtml'
        # default False
        self.enable_branch_coverage = False
        self.lcov_follow_links = False
    
    def validate(self):
        if not self.lcov_path:
            return InvalidOpts("must set lcov_path, got empty string")
        if not self.gen_html_path:
            return InvalidOpts("must set gen_html_path, got empty string")
        if not self.fuzzer_path:
            return InvalidOpts("must set fuzzer_path, got empty string")
        if not self.source_dir:
            return InvalidOpts("must set source_dir, got empty string")
        if not self.output_dir:
            return InvalidOpts("must set output_dir, got empty string")
        if not self.lcov_output_dir:
            return InvalidOpts("must set lcov_output_dir, got empty string")
        if not self.gen_html_output_dir:
            return InvalidOpts("must set gen_html_output_dir, got empty string")
        if not self.gen_html_output_dir:
            return InvalidOpts("must set gen_html_output_dir, got empty string")
        return None

def parse_cmdline():

    # opts.output_dir = os.path.realpath('.material/fuzz-cov')

    p = argparse.ArgumentParser()
    p.prog = 'fuzzer_cov.commands.libfuzzer'

    p.add_argument("--fuzzer", type=str, required=True,
        help="Fuzzer Path (gcov instrumented)")
    p.add_argument("-s", "--src", type=str, required=True,
        help="Source root directory")
    p.add_argument("-o", "--out", type=str, required=True,
        help="Coverage output directory")
    p.add_argument("-c", "--corpus-dir", type=str, required=True,
        help="Corpus (inputs) Directory")

    p.add_argument("--lcov-follow-links", action='store_true', default=False,
        help="Follow links when searching .da files")
    p.add_argument("--enable-branch-coverage", action='store_true', default=False,
        help="Include branch coverage in code coverage reports (may be slow)")
    p.add_argument("--lcov-exclude-pattern", type=str, default="/usr/include/\\*",
        help="Set exclude pattern for lcov results")
    
    p.add_argument("--lcov-path", type=str,
            help="Path to lcov command", default="/usr/bin/lcov")
    p.add_argument("--gen-html-path", type=str,
            help="Path to genhtml command", default="/usr/bin/genhtml")
    
    p.add_argument("-v", "--verbose", action='store_true',
            help="Verbose mode", default=False)
    p.add_argument("-V", "--version", action='store_true',
            help="Print version and exit", default=False)
    p.add_argument("-q", "--quiet", action='store_true',
            help="Quiet mode", default=False)

    # p.add_argument("--disable-coverage-init", action='store_true',
    #         help="Disable initialization of code coverage counters at afl-cov startup",
    #         default=False)

    # p.add_argument("--gcov-check", action='store_true',
    #         help="Check to see if there is a binary in --coverage-cmd (or in --gcov-check-bin) has coverage support",
    #         default=False)
    # p.add_argument("--gcov-check-bin", type=str,
    #         help="Test a specific binary for code coverage support",
    #         default=False)
    # p.add_argument("--disable-gcov-check", type=str,
    #         help="Disable check for code coverage support",
    #         default=False)

    # p.add_argument("-O", "--overwrite", action='store_true',
    #         help="Overwrite existing coverage results", default=False)
    # p.add_argument("--validate-args", action='store_true',
    #         help="Validate args and exit", default=False)

    return p.parse_args()

def get_fuzzer_cov_opts_from_command_line_options(opts: Opts, args: object):
    opts.lcov_path = args.lcov_path
    opts.gen_html_path = args.gen_html_path

    opts.fuzzer_path = args.fuzzer
    opts.source_dir = args.src
    opts.output_dir = args.out
    
    opts.lcov_exclude_pattern = args.lcov_exclude_pattern
    opts.enable_branch_coverage = args.enable_branch_coverage
    opts.lcov_follow_links = args.lcov_follow_links

    opts.lcov_output_dir = os.path.join(opts.output_dir, 'lcov')
    opts.gen_html_output_dir = os.path.join(opts.output_dir, 'web')

    maybe_err = opts.validate()
    if maybe_err is not None:
        raise maybe_err # pylint: disable-msg=E0702

def main():
    # Setup Environment Values
    args = parse_cmdline()
    opts = Opts()
    get_fuzzer_cov_opts_from_command_line_options(opts, args)

    clean = True

    # create container
    container = BuildContainerImpl(opts)
    container.register_impl(LoggerImpl, Logger)
    container.register_impl(CommandExecutorImpl, CommandExecutor)
    container.register_impl(LibFuzzerInstanceExecutor, FuzzerExecutor)
    container.register_impl(LCovRunner)
    container.register_impl(LCovOutputPathPolicy)
    container.register_impl(GenHtmlRunner)
    container.register_impl(GenHtmlOutputPathPolicy)

    # create lcov components
    lcov_path_policy = container.resolve(LCovOutputPathPolicy)
    gen_html_path_policy = container.resolve(GenHtmlOutputPathPolicy)
    fuzzer_instance = container.resolve(FuzzerExecutor)
    lcov_runner = container.resolve(LCovRunner)
    gen_html_runner = container.resolve(GenHtmlRunner)

    # main logic
    cov_output_path = Path(opts.output_dir)
    cov_output_path.mkdir(parents=True, exist_ok=True)

    lcov_path_policy.initialize_file_structure(clean=clean)
    gen_html_path_policy.initialize_file_structure(clean=clean)

    lcov_runner.init_coverage_files(lcov_path_policy, silent=0)
    fuzzer_instance.exec_corpus_set(args.corpus_dir, silent=0)
    lcov_runner.collect_coverage(lcov_path_policy, silent=0)

    gen_html_path_policy.use_lcov_path_policy(lcov_path_policy)
    gen_html_runner.gen_cov_report(gen_html_path_policy, silent=0)

if __name__ == '__main__':
    main()
