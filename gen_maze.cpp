#include<bits/stdc++.h>
using namespace std;

void add_edge(vector<int> *g, int u, int v)
{
  g[u].push_back(v);
  g[v].push_back(u);
}

void prim(vector<int> *g, vector<int> *dest, int v_n)
{
  int v, visited[v_n]={0};
  queue<int> todo;

  todo.push(0);
  visited[0] = true;
  do
  {
    v = todo.front();
    todo.pop();
    for (int i=0; i < g[v].size(); ++i)
    {
      if (visited[g[v][i]]) continue;
      todo.push(g[v][i]);
      add_edge(dest, v, g[v][i]);
      visited[g[v][i]]=true;
    }
  } while (!todo.empty());
}

void print_graph(vector<int> *g, int v_n)
{
  for (int i=0; i < v_n; ++i)
  {
    //cout << i << ": ";
    for (int j=0; j < g[i].size(); ++j)
    {
      cout << g[i][j] << ' ';
    }
    cout << endl;
  }
}

void create_grid(vector<int> *dest, int w, int h)
{
  if (!w || !h) return;

  for (int i=0; i < w-1; ++i)
  {
    add_edge(dest, i, i+1);
  }

  for (int i=0; i < h-1; ++i)
  {
    add_edge(dest, i*w, (i+1) * w);
  }

  if (h == 1) return;

  for (int i=0; i < w-1; ++i)
  {
    add_edge(dest, w*(h-1) + i, w*(h-1) + i+1);
  }

  if (w == 1) return;
  for (int i=0; i < h-1; ++i)
  {
    add_edge(dest, w-1 + i*w, w-1 + (i+1) * w);
  }

  int u;
  for (int x=1; x < w-1; ++x)
  {
    for (int y=1; y < h-1; ++y)
    {
      u = y*w + x;
      add_edge(dest, u, u-1);
      add_edge(dest, u, u+1);
      add_edge(dest, u, u-w);
      add_edge(dest, u, u+w);
    }
  }
}

int main()
{
  int w=15, h=6;
  vector<int> grid[w*h];
  vector<int> tree[w*h];

  create_grid(grid, w, h);
  prim(grid, tree, w*h);

  //print_graph(grid, w*h);
  print_graph(tree, w*h);

  return 0;
}
