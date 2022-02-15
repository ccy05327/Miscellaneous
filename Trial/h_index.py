def h_index(n, citations):
    ans = []
    # TODO: Complete the function to get the H-Index scores after each paper

    return ans


if __name__ == '__main__':
    T = int(input())

    for test_case in range(1, T + 1):
        N = int(input())  # The number of papers
        for i in N:
            # The number of citations for each paper
            citations = map(int, input().split())
            print('citations:', citations)
        h_index_scores = h_index(N, citations)
        print('h_index:', h_index)
        print("Case #" + str(test_case) + ": " +
              ' '.join(map(str, h_index_scores)))
