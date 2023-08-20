# This directory contains some visualizations

## char-freq

This visuzation shows character frequency visualizations.

- height corresponds to how many times the character was used
- color gradient shows overall frequency in Chinese
- built in blender
- exported as .glb file
- embedded in html using View3D-vue

To create:

```
npm create vue@latest
```

- name: char-freq
- default options for everything else
- cd char-freq

```
npm install @egjs/vue3-view3d
```

```
import Viz from './components/Viz.vue'
```

```
  <viz />
```

```
npm run dev
```

===Checkpoint===


- Move `blocks.glb` to public dir

Function to arrange all characters into rows and columns:

```py
def main(arr, r_len, c_len):
    diff = len(arr) - (r_len * c_len)
    if diff >= 0:
        arr = arr[:r_len*c_len]
        ret_arr = []
        for c in range(c_len):
            sub_arr = []
            for r in range(r_len):
                sub_arr.append(arr[c*r_len + r])
            ret_arr.append(sub_arr)
        return ret_arr
    else:
        raise Exception("array too short")

main([1,2,3,4,5,6,7,8,9], 2, 3)
```

File size is near 60MB with 20x20 characters