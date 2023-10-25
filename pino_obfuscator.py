#!/usr/bin/env python3
import argparse
import random
import sys

sep = "@@SEP@@"

def main(delta, solutions, signed=False, randomize=False, float_=False):

  if signed :
    solutions = 2**(solutions-1) - 1
  else :
    solutions = 2**(solutions) - 1

  total_space = solutions
  start_ea = 0 if not signed else -total_space
  stop_ea = total_space
  vname = "i"

  output = []
  output_end = []
  space = ""
  next = 0

  to_range = total_space // delta
  if signed :
    to_range *= 2

  for x in range(to_range) :
    if next == 0:
      output_tmp = space + "if ({} > {})".format(vname, start_ea) + "{"
      if float_ :
        output_tmp = space + "if ({} > {}.1337)".format(vname, start_ea) + "{"

      output.append(output_tmp)
      start_ea += delta
      next = 1

    else :
      output_tmp = space + "if ({} < {})".format(vname, stop_ea) + "{"
      if float_ :
        output_tmp = space + "if ({} < {}.1337)".format(vname, stop_ea) + "{"

      output.append(output_tmp)
      stop_ea -= delta
      next = 0
  
  stop_ea += delta
  start_ea -= delta

  if randomize :
    random.shuffle(output)

  for x in range(len(output)) :
    space += "  "
    output_end.append(space + "}")
    output[x] = space + output[x]

  space += "  "
  output.append(space + "puts(\"You win!\");")

  space_solutions = [start_ea, stop_ea]
  if not float_ :
    space_solutions[0] += 1
    space_solutions[1] -= 1
  else :
    space_solutions[0] = float(space_solutions[0])
    space_solutions[1] = float(space_solutions[1])

  return space_solutions, len(output), "\n".join(["\n".join(output), "\n".join(output_end[::-1]), ""])


def get_source_code_example(is_signed=False, is_float=False) :
  main_s = [ \
    """
      #include <stdio.h>
      int main(int argc){
        char buff[32] = {0};
        unsigned int i;
        fgets(buff, 32, stdin);
        i = atoi(buff);

        // paste from here the obfuscated code
        @@SEP@@
      }
    """ ,\
    """
      #include <stdio.h>
      int main(int argc){
        char buff[32] = {0};
        int i;
        fgets(buff, 32, stdin);
        i = atoi(buff);

        // paste from here the obfuscated code
        @@SEP@@
      }
    """ ,\
    """
      #include <stdio.h>
      
      int main(int argc){
      
        char buff[32] = {0};
        double i;
        fgets(buff, 32, stdin);
        sscanf(buff, "%lf", &i);
        
        // paste from here the obfuscated code
        @@SEP@@
      }
    """
  ]
  idx = 1 if is_signed else 0
  idx = 2 if is_float else idx
  return main_s[idx]


if __name__ == "__main__" :
  parser = argparse.ArgumentParser(
    prog='pino_obfuscator',
    description="""
      The script combines multiple IFs in order to add a sort of code
      obfuscation. To solve all the innested IFs a user should insert a valid
      number that is inside the solution space and that will pass each IF.
    """,
    epilog='',
  )

  parser.add_argument("-d", "--delta", default=8000000, type=int, help="This value is used to increase or decrease the space of solutions (default: 8000000, [1, ...])")
  parser.add_argument("-s", "--solutions", default=32, help="Define the space of solutions by the number of bits. (defualt:32, max:64)")
  parser.add_argument("-n", "--negative", action="store_true", default=False, help="Use signed numbers (default:false)")
  parser.add_argument("-w", "--write_into", default="output.c", help="Output (default:'output.c')")
  parser.add_argument("-r", "--randomize", action="store_true", default=False, help="Randomize IF blocks positions")
  parser.add_argument("-f", "--float", action="store_true", default=False, help="Use floating numbers instead of integers (default:false)")
  args = parser.parse_args()

  delta = args.delta 
  solutions = args.solutions
  signed = args.negative

  assert(delta > 0)
  assert(solutions <= 64)
  assert(solutions >= 8)

  if delta < 1000000:
    print("You are inserting a delta lower than 1000000, this could take a notable amount of time from the cpu")
    rets = input("Continue? (y/N)").strip()
    if rets.lower() != "y" :
        print("exit")
        sys.exit(0)

  (a, b), inner_line, output = main(delta, solutions, signed=signed, randomize=args.randomize, float_=args.float)

  output = get_source_code_example(is_signed=args.negative, is_float=args.float).replace(sep, output)

  with open(args.write_into, "w") as fp:
    fp.write(output)

  print("File saved '{}', \"You win!\" line:'{}'".format(args.write_into, inner_line))
  print("Space of solutions: [{}, {}]".format(a,b))
  print("[+] Done")


