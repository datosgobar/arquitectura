
import argparse


class ModuleBase:
    prog_text = "MODULE"
    desc_text = "Generic module"
    input_text = "Input"
    output_text = "Output"
    conf_text = "Configuration"
    epilog_text = None
    input_required = False
    output_required = False
    conf_required = False

    def run(self):
        parser = argparse.ArgumentParser(description=self.desc_text,
                                         prog=self.prog_text,
                                         epilog=self.epilog_text)
        parser.add_argument('--input', type=str, help=self.input_text,
                            default=None, required=self.input_required)
        parser.add_argument('--output', type=str, help=self.output_text,
                            default=None, required=self.output_required)
        parser.add_argument('--conf', type=str, help=self.conf_text,
                            default=None, required=self.conf_required)
        args = parser.parse_args()
        self.implementation(**args.__dict__)

    def implementation(self, input=None, output=None, conf=None):
        print "--input %s --output %s --conf %s" % (input, output, conf)
        raise NotImplemented
