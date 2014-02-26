__kernel void opticalflowkernel(__global int *image1, 
                                __global int *image2, 
                                int imagesize,
                                int windowsize,
                                // results
                                __global int *fx,
                                __global int *fy){
  // kernel for computing the optical flow
  // uses brute force; one thread per pixel
  // no shared memory
  // uses a window to compare the sum of squared differences
  // we use a rectangular grid with the same size as the image
  int row = get_global_id(1);
  int col = get_global_id(0);

  if(row > imagesize || col > imagesize) return;

  int bfirstconvolve = 1;
  float mincost = 1000000.0f;
  int frow = 0;
  int fcol = 0;
  int rw, cw, ii, jj, row_image1, row_image2, col_image1, col_image2;
  float cost;
  int val_image1;
  int val_image2;
  for(rw = -windowsize; rw <= windowsize; rw++)
    for(cw = -windowsize; cw <= windowsize; cw++){
      // compute the difference
      cost = 0.0f;
      for(ii = -windowsize; ii <= windowsize; ii++)
        for(jj = -windowsize; jj <= windowsize; jj++){
          row_image2 = row + rw + ii;
          col_image2 = col + cw + jj;
          row_image1 = row + ii;
          col_image1 = col + jj;
          val_image2 = (row_image2 >= 0 && row_image2 < imagesize && col_image2 >= 0 && col_image2 < imagesize) ?
                                                           image2[row_image2 * imagesize + col_image2] : 0;
          val_image1 = (row_image1 >= 0 && row_image1 < imagesize && col_image1 >= 0 && col_image1 < imagesize) ?
                                                           image1[row_image1 * imagesize + col_image1] : 0;
          cost = cost + (float)((val_image1 - val_image2)*(val_image1 - val_image2));
          }
      cost = cost / (float)((2 * windowsize + 1) * (2 * windowsize + 1));
      if(bfirstconvolve == 1){
        bfirstconvolve = 0;
        mincost = cost;
        frow = rw;
        fcol = cw;
        }
      else if(cost <= mincost){
	mincost = cost;
        frow = rw;
        fcol = cw;
        }
      }
  fy[row * imagesize + col] = frow;
  fx[row * imagesize + col] = fcol;
  return;
}

