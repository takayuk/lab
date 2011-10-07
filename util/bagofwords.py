# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-


def bagofwords(sentence, target_feature):

    import subprocess, re, os
    
    do_mecab_dir = os.path.abspath(os.path.dirname(__file__))
    cmdline = "%s/do_mecab %s" % (do_mecab_dir, sentence)
    cwd = "."

    subproc = subprocess.Popen(cmdline, shell = True, cwd = cwd,
            stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
            close_fds = True)

    (stdouterr, stdin) = (subproc.stdout, subproc.stdin)

    words = []
    
    while True:
        line = stdouterr.readline()
        if not line: break

        try:
            node = line.split("\t")

            (surface, feature) = (node[0], node[1])
            for feat in feature.split(','):

                if feat in target_feature:
                    words.append((surface, feature))

        except UnicodeDecodeError: break
        except IndexError: pass

    return words


if __name__ == "__main__":
    
    doc = "今日はよく晴れ、絶好のお花見日和となりました。"
    bow = bagofwords(sentence = doc, target_feature = ["名詞"])
    for word in bow:
        print('%s, %s' % (word[0], word[1]))

