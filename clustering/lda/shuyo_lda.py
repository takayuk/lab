# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import numpy
import vocabulary


class LDA:
    """LDA : collapsed Gibbs で推論"""
    def __init__(self, K, alpha, beta):
        self.K = K
        self.alpha = alpha # parameter of topics prior
        self.beta = beta   # parameter of words prior

    def set_corpus(self, corpus, stopwords = 0):
        """コーパスの読み込みとカウンタの初期化"""
        voca = vocabulary.Vocabulary(stopwords==0)
        self.docs = [voca.doc_to_ids(doc) for doc in corpus]

        M = len(self.docs)
        self.V = voca.size()

        print('V: %d' % self.V)

        self.z_m_n = [] # topics of words of documents
        self.n_m_z = numpy.zeros((M, self.K)) + self.alpha     # word count of each document and topic
        self.n_z_t = numpy.zeros((self.K, self.V)) + self.beta # word count of each topic and vocabulary
        self.n_z = numpy.zeros(self.K) + self.V * self.beta    # word count of each topic

        self.N = 0
        for m, doc in enumerate(self.docs):
            self.N += len(doc)
            z_n = numpy.random.randint(0, self.K, len(doc))
            self.z_m_n.append(z_n)
            for t, z in zip(doc, z_n):
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
        return voca

    def inference(self):
        """イテレーション1回分の推論を行う"""
        for m, doc in enumerate(self.docs):
            z_n = self.z_m_n[m]
            for n, t in enumerate(doc):
                # n 番目の単語 t (トピック z)についてカウンタを減算
                z = z_n[n]
                self.n_m_z[m, z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                # トピックの事後分布からサンプリング
                p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()

                # サンプリングされた新トピックを設定＆カウンタを増加
                z_n[n] = new_z
                self.n_m_z[m, new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def worddist(self):
        """トピック-単語分布を返す"""
        return self.n_z_t / self.n_z[:, numpy.newaxis]

    def perplexity(self):
        """パープレキシティを計算"""
        phi = self.worddist()
        log_per = 0
        Kalpha = self.K * self.alpha
        for m, doc in enumerate(self.docs):
            theta = self.n_m_z[m,:] / (len(doc) + Kalpha)
            for w in doc:
                log_per -= numpy.log(numpy.inner(phi[:,w], theta))
        return numpy.exp(log_per / self.N)

if __name__ == '__main__':


    voca = vocabulary.Vocabulary()
    #docs = [ voca.doc_to_ids(doc) for doc in vocabulary.read_from('corpus_1') ]
    corpus = vocabulary.read_from('corpus_1')

    lda = LDA(K = 10, alpha = 0.5, beta = 0.5)
    lda.set_corpus(corpus)

    for i in range(20):

        lda.inference()

        print(lda.perplexity())

    phi = lda.worddist()
    print(phi[0])
    print(lda.n_z)
    print(lda.n_z_t)
    print(lda.n_m_z)

