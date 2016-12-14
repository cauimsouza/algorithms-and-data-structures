public class Stack<Item>{
	private Item[] s;
	private int N = 0;

	public Stack(){
		s = (Item[]) new Object[1];
	}

	public boolean isEmpty(){
		return N == 0;
	}

	public void push(Item item){
		if(N == s.length) resize(2 * N);
		s[N++] = item;
	}

	private void resize(int capacity){
		Item[] copy = (Item[]) new Object[capacity];
		for(int i = 0; i < N; i++)
			copy[i] = s[i];
		s = copy;
	}

	public Item pop(){
		if(N == 0) return null;
		Item item = s[--N];
		s[N] = null;
		if(N > 0 && N == s.length/4) resize(s.length/2);
		return item;
	}
}