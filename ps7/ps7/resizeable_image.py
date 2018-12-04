import math
import imagematrix


class ResizeableImage(imagematrix.ImageMatrix):
    
    def best_seam(self):
        # cache image
        energy = dict()
        for w in range(self.width):
            for h in range(self.height):
                energy[w, h] = self.energy(w, h)

        dp = dict()
        parents = dict()
        for j in range(self.height):
            for i in range(self.width):
                if j == 0:
                    # build bottom
                    dp[i, j] = energy[i, j]
                    continue

                # dp[i, j] = min(dp(i-1, j-1), dp(i, j-1), dp(i+1, j-1)) + energy(i, j)
                # memoize upper row according to recurrence
                # down, base case
                dp[i, j] = dp[i, j-1] + energy[i, j]
                parents[i, j] = i, j-1
                
                # down-left
                if i != 0 and dp[i, j] > dp[i-1, j-1] + energy[i, j]:
                    dp[i, j] = dp[i-1, j-1] + energy[i, j]
                    parents[i,j] = i-1, j-1

                # down-right
                if i != self.width-1 and dp[i, j] > dp[i+1, j-1] + energy[i, j]:
                    dp[i, j] = dp[i+1, j-1] + energy[i, j]
                    parents[i,j] = i+1, j-1
                
        # pick best seam
        best_seam = math.inf
        i = None
        for iter_i in range(self.width):
            if best_seam > dp[iter_i, self.height-1]:
                best_seam = dp[iter_i, self.height-1]
                i = iter_i

        # create seam
        # add initial pixel and crawl through parents
        seam = list()
        seam.append((i, self.height-1))
        for j in reversed(range(1, self.height)):
            seam.append(parents[i, j])
            i = seam[-1][0]

        return seam
                
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
