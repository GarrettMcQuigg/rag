import { Component, ElementRef, ViewChild, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  private http = inject(HttpClient);

  messages: Message[] = [];
  inputText = '';
  isLoading = false;

  private apiUrl = 'http://localhost:8000/api/ask';

  sendMessage(): void {
    if (!this.inputText.trim() || this.isLoading) return;

    const userMessage = this.inputText.trim();
    this.messages.push({ role: 'user', content: userMessage });
    this.inputText = '';
    this.isLoading = true;

    this.http.post<{ answer: string }>(this.apiUrl, {
      query: userMessage,
      history: this.messages.slice(-6)
    }).subscribe({
      next: (response) => {
        this.messages.push({ role: 'assistant', content: response.answer });
        this.scrollToBottom();
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error:', error);
        this.messages.push({ role: 'assistant', content: 'Sorry, something went wrong.' });
        this.isLoading = false;
      }
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      if (this.messagesContainer) {
        const element = this.messagesContainer.nativeElement;
        element.scrollTop = element.scrollHeight;
      }
    }, 100);
  }

  autoGrow(textarea: HTMLTextAreaElement): void {
    textarea.style.height = 'auto';

    const newHeight = textarea.scrollHeight;
    textarea.style.height = `${newHeight}px`;
  }

  useSuggestion(question: string): void {
    this.inputText = question;
    this.sendMessage();
  }

  handleKeydown(event: KeyboardEvent, textarea: HTMLTextAreaElement): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
      this.autoGrow(textarea);
    }
  }

  startNewChat(): void {
    this.messages = [];
    this.inputText = '';
    this.isLoading = false;
  }
}